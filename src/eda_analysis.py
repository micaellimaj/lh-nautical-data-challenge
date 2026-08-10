import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
SQL_PATH = BASE_DIR / "sql" / "01_eda_orders.sql"

def read_sql_file(file_path: Path) -> str:
    """Lê o conteúdo de um arquivo .sql."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def run_q1_eda():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco de dados não encontrado em {DB_PATH}. Execute setup_database.py primeiro.")

    con = duckdb.connect(str(DB_PATH))

    # Carrega e executa a query SQL do arquivo externo
    query_sql = read_sql_file(SQL_PATH)
    
    print("\n--- [QUESTÃO 1.1] EXECUÇÃO DA QUERY SQL (VIA ARQUIVO .SQL) ---")
    result = con.execute(query_sql).df()
    print(result.to_string(index=False))

    # Obter total de colunas da tabela orders
    total_colunas = con.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'orders'").fetchone()[0]
    
    print("\n--- [QUESTÃO 1 - PARTE 1 & 2] RESUMO DA TABELA ORDERS ---")
    print(f"Total de Linhas: {result['total_linhas'][0]:,}")
    print(f"Total de Colunas: {total_colunas}")
    print(f"Intervalo de Datas: {result['data_minima'][0]} até {result['data_maxima'][0]}")
    print(f"Valor Mínimo (Total): R$ {result['valor_minimo'][0]:,.2f}")
    print(f"Valor Máximo (Total): R$ {result['valor_maximo'][0]:,.2f}")
    print(f"Valor Médio (Total): R$ {result['valor_medio'][0]:,.2f}")

    con.close()

if __name__ == "__main__":
    run_q1_eda()