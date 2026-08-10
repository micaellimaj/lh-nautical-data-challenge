import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
SQL_PATH = BASE_DIR / "sql" / "02_q3_validation.sql"

def validate_q3_2():
    con = duckdb.connect(str(DB_PATH))
    
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        query_sql = f.read()

    print("\n--- [QUESTÃO 3.2] VALIDAÇÃO DE VOLUMETRIA ---")
    result = con.execute(query_sql).df()
    print(result.to_string(index=False))
    
    print("\n" + "="*50)
    print(f"TOTAL DE LINHAS SOMADAS: {result['total_linhas_somadas'][0]:,}")
    print("="*50 + "\n")
    
    con.close()

if __name__ == "__main__":
    validate_q3_2()