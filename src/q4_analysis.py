import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
SQL_PATH = BASE_DIR / "sql" / "03_q4_analysis.sql"

def run_q4_analysis():
    if not SQL_PATH.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado em: {SQL_PATH}")

    # Lê o arquivo SQL mantendo a pasta sql/ como única fonte da verdade
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Separa as queries do arquivo SQL pelo ponto e vírgula
    queries = [q.strip() for q in sql_content.split(";") if q.strip()]

    con = duckdb.connect(str(DB_PATH))

    print("\n" + "="*70)
    print("--- [QUESTÃO 4.1] TOP 10 CLIENTES DE ELITE (DIVERSIDADE >= 13 CATEGORIAS) ---")
    print("="*70)
    df_top_10 = con.execute(queries[0]).df()
    print(df_top_10.to_string(index=False))

    print("\n" + "="*70)
    print("--- [QUESTÃO 4.2] CATEGORIA MAIS CONSUMIDA PELOS TOP 10 CLIENTES ---")
    print("="*70)
    df_top_cat = con.execute(queries[1]).df()
    print(df_top_cat.to_string(index=False))
    print("="*70 + "\n")

    con.close()

if __name__ == "__main__":
    run_q4_analysis()