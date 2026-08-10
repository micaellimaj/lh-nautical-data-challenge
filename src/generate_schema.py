import csv
import os
import re
from datetime import datetime
from pathlib import Path

# Caminhos base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "lh_nautical_csv"
OUTPUT_SQL_FILE = BASE_DIR / "sql" / "schema.sql"

def infer_postgres_type(val_str: str) -> str:
    """Infera o tipo de dado do PostgreSQL baseado na string de um valor individual."""
    val_str = val_str.strip()
    
    if not val_str:
        return "NULL"
    
    # 1. Checagem de Booleano
    if val_str.lower() in ("true", "false", "t", "f", "1", "0"):
        return "BOOLEAN"
    
    # 2. Checagem de Inteiro
    if re.match(r"^-?\d+$", val_str):
        if len(val_str) > 18:
            return "VARCHAR(255)"
        val_int = int(val_str)
        if -2147483648 <= val_int <= 2147483647:
            return "INTEGER"
        return "BIGINT"
    
    # 3. Checagem de Ponto Flutuante / Decimal
    if re.match(r"^-?\d+\.\d+$", val_str):
        return "NUMERIC(14, 2)"
    
    # 4. Checagem de Timestamp
    datetime_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    for fmt in datetime_formats:
        try:
            datetime.strptime(val_str, fmt)
            return "TIMESTAMP"
        except ValueError:
            pass

    # 5. Checagem de Data
    date_formats = ["%Y-%m-%d", "%d/%m/%Y"]
    for fmt in date_formats:
        try:
            datetime.strptime(val_str, fmt)
            return "DATE"
        except ValueError:
            pass

    return "VARCHAR"

def resolve_type_priority(current_type: str, new_type: str) -> str:
    """Combina tipos de dados para uma mesma coluna garantindo que o tipo seja abrangente."""
    if new_type == "NULL":
        return current_type
    if current_type == "NULL":
        return new_type
    if current_type == new_type:
        return current_type
    
    # Hierarquia de promoção de tipos
    # Se houver conflito entre INTEGER e NUMERIC -> vira NUMERIC
    if {current_type, new_type} <= {"INTEGER", "BIGINT", "NUMERIC(14, 2)"}:
        if "NUMERIC(14, 2)" in (current_type, new_type):
            return "NUMERIC(14, 2)"
        return "BIGINT"
    
    # Se houver conflito entre DATE e TIMESTAMP -> vira TIMESTAMP
    if {current_type, new_type} <= {"DATE", "TIMESTAMP"}:
        return "TIMESTAMP"
        
    # Qualquer incompatibilidade maior (ex: VARCHAR vs INT) força o tipo mais seguro (TEXT / VARCHAR)
    return "VARCHAR(255)"

def generate_ddl_for_csv(csv_path: Path) -> str:
    """Lê um arquivo CSV usando a biblioteca nativa csv e infere o comando CREATE TABLE."""
    table_name = csv_path.stem.lower()
    
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return f"-- Tabela {table_name} vazia.\n"
        
        # Limpa nomes das colunas
        headers = [h.strip().lower().replace(" ", "_").replace("-", "_") for h in headers]
        column_types = {h: "NULL" for h in headers}
        
        # Analisa até 1000 linhas por performance e precisão de amostragem
        for row_idx, row in enumerate(reader):
            if row_idx >= 1000:
                break
            for col_idx, cell_value in enumerate(row):
                if col_idx < len(headers):
                    col_name = headers[col_idx]
                    inferred = infer_postgres_type(cell_value)
                    column_types[col_name] = resolve_type_priority(column_types[col_name], inferred)

    # Monta as definições de colunas
    col_definitions = []
    for col_name, inferred_type in column_types.items():
        final_type = "VARCHAR(255)" if inferred_type == "NULL" else inferred_type
        col_definitions.append(f"    {col_name} {final_type}")
    
    ddl = f"-- Drop & Create Table para: {table_name}\n"
    ddl += f"DROP TABLE IF EXISTS {table_name} CASCADE;\n"
    ddl += f"CREATE TABLE {table_name} (\n"
    ddl += ",\n".join(col_definitions)
    ddl += "\n);\n\n"
    
    return ddl

def main():
    if not RAW_DATA_DIR.exists():
        print(f"Erro: O diretório {RAW_DATA_DIR} não existe.")
        return

    csv_files = sorted(list(RAW_DATA_DIR.glob("*.csv")))
    
    if not csv_files:
        print(f"Nenhum arquivo CSV encontrado em {RAW_DATA_DIR}")
        return

    print(f"Iniciando a inferência de schema nativa para {len(csv_files)} arquivos CSV...")

    OUTPUT_SQL_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_SQL_FILE, mode="w", encoding="utf-8") as out_f:
        out_f.write("-- ========================================================\n")
        out_f.write("-- SCHEMA DDL GERADO AUTOMATICAMENTE VIA PYTHON NATURO\n")
        out_f.write(f"-- Data de Geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_f.write("-- PostgreSQL Compatible\n")
        out_f.write("-- ========================================================\n\n")

        for csv_file in csv_files:
            print(f"Processando: {csv_file.name}...")
            ddl_statement = generate_ddl_for_csv(csv_file)
            out_f.write(ddl_statement)

    print("=" * 60)
    print(f"SUCESSO! O arquivo DDL final foi gerado em:\n -> {OUTPUT_SQL_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()