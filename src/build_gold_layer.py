import logging
import duckdb
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
GOLD_SQL_PATH = BASE_DIR / "sql" / "create_gold_layer.sql"
GOLD_DIR = BASE_DIR / "data" / "gold"

def build_gold_layer():
    if not DB_PATH.exists():
        logging.error(f"Banco Silver não encontrado em {DB_PATH}")
        return

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    logging.info("Construindo a Camada Gold no DuckDB...")

    with open(GOLD_SQL_PATH, "r", encoding="utf-8") as f:
        gold_sql = f.read()

    queries = [q.strip() for q in gold_sql.split(";") if q.strip()]
    for query in queries:
        con.execute(query)

    tables = con.execute("SHOW TABLES;").fetchall()
    gold_tables = [t[0] for t in tables if t[0].startswith("gold_")]

    logging.info("Exportando tabelas Gold para arquivos CSV em data/gold/...")
    for table in gold_tables:
        csv_out = GOLD_DIR / f"{table}.csv"
        con.execute(f"COPY {table} TO '{csv_out.as_posix()}' (HEADER, DELIMITER ',');")
        logging.info(f"Arquivo gerado: {csv_out.name}")

    logging.info("=" * 60)
    logging.info("CAMADA GOLD EXPORTADA COM SUCESSO!")
    logging.info(f"Arquivos salvos em: {GOLD_DIR}")
    logging.info("=" * 60)

    con.close()

if __name__ == "__main__":
    build_gold_layer()