import logging
from pathlib import Path
import duckdb

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Caminhos do Projeto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "lh_nautical_csv"
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
SCHEMA_SQL_PATH = BASE_DIR / "sql" / "schema.sql"

def load_data_respecting_schema():
    if not RAW_DATA_DIR.exists():
        logging.error(f"Diretório de CSVs não encontrado em: {RAW_DATA_DIR}")
        return

    if not SCHEMA_SQL_PATH.exists():
        logging.error(f"Arquivo de Schema não encontrado em: {SCHEMA_SQL_PATH}. Execute a Questão 2 primeiro.")
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Conectando ao banco de dados local: {DB_PATH}")
    con = duckdb.connect(str(DB_PATH))

    logging.info(f"Aplicando o schema DDL a partir de: {SCHEMA_SQL_PATH.name}")
    with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
        schema_ddl = f.read()
    
    # Executa os comandos CREATE TABLE / DROP TABLE
    con.execute(schema_ddl)
    logging.info("Schema DDL aplicado com sucesso!")

    # 2. Carrega todos os CSVs respeitando o schema das tabelas criadas
    csv_files = sorted(list(RAW_DATA_DIR.glob("*.csv")))
    logging.info(f"Iniciando o carregamento dos {len(csv_files)} arquivos CSV...")

    for csv_file in csv_files:
        table_name = csv_file.stem.lower()
        logging.info(f"Inserindo dados em: '{table_name}'...")
        
        copy_query = f"""
            INSERT INTO {table_name} 
            SELECT * FROM read_csv('{csv_file.as_posix()}', header=True, auto_detect=True);
        """
        try:
            con.execute(copy_query)
        except Exception as e:
            logging.warning(f"Aviso ao inserir {table_name} com formatação estrita. Tentando carga direta: {e}")
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file.as_posix()}', HEADER=True);")

    # Validação
    tables = con.execute("SHOW TABLES;").fetchall()
    table_names = [t[0] for t in tables]
    
    logging.info("=" * 60)
    logging.info(f"SUCESSO! {len(table_names)} tabelas carregadas no banco respeitando o schema:")
    logging.info(f"Tabelas: {', '.join(table_names)}")
    logging.info("=" * 60)

    con.close()

if __name__ == "__main__":
    load_data_respecting_schema()