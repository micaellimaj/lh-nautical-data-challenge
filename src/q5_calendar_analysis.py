import duckdb
from pathlib import Path

# Definição dos caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"
SQL_PATH = BASE_DIR / "sql" / "04_q5_calendar_dimension.sql"

def run_q5_analysis():
    if not SQL_PATH.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado em: {SQL_PATH}")

    # Lê o arquivo SQL mantendo a pasta sql/ como única fonte da verdade
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Separa as queries do arquivo SQL pelo ponto e vírgula
    queries = [q.strip() for q in sql_content.split(";") if q.strip()]

    con = duckdb.connect(str(DB_PATH))

    print("\n" + "="*80)
    print("--- [QUESTÃO 5] ANÁLISE DE VENDAS DIÁRIAS POR DIA DA SEMANA (DIMENSÃO DE CALENDÁRIO) ---")
    print("="*80)
    
    # Executa a query principal contida em 04_q5_calendar_dimension.sql
    df_q5 = con.execute(queries[0]).df()
    
    # Formata valores numéricos para melhor exibição no terminal
    if not df_q5.empty:
        if 'faturamento_total' in df_q5.columns:
            df_q5['faturamento_total'] = df_q5['faturamento_total'].map("R$ {:,.2f}".format)
        if 'media_vendas_diaria' in df_q5.columns:
            df_q5['media_vendas_diaria'] = df_q5['media_vendas_diaria'].map("R$ {:,.2f}".format)

    print(df_q5.to_string(index=False))
    print("="*80 + "\n")

    con.close()

if __name__ == "__main__":
    run_q5_analysis()