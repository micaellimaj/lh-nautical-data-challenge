import duckdb
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"

def run_q6_forecast():
    con = duckdb.connect(str(DB_PATH))

    # Query filtrando vendas válidas e agrupando por mês
    query = """
    SELECT 
        DATE_TRUNC('month', CAST(o.placed_at AS DATE)) AS mes,
        SUM(CAST(oi.quantity AS INTEGER)) AS qtd_real
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    WHERE LOWER(p.name) LIKE '%bússola de bordo 702%'
      AND LOWER(o.status) NOT IN ('cancelled', 'canceled')
    GROUP BY DATE_TRUNC('month', CAST(o.placed_at AS DATE))
    ORDER BY mes ASC;
    """
    df = con.execute(query).df()
    con.close()

    df['mes'] = pd.to_datetime(df['mes'])

    # Garante a continuidade mês a mês sem lacunas temporais
    full_idx = pd.date_range(start=df['mes'].min(), end=df['mes'].max(), freq='MS')
    df = df.set_index('mes').reindex(full_idx, fill_value=0).rename_axis('mes').reset_index()

    # Cálculo da Média Móvel dos últimos 3 meses (Sem Data Leakage)
    # .shift(1) garante que o mês t use apenas os dados dos meses t-1, t-2 e t-3
    df['previsao_baseline'] = (
        df['qtd_real']
        .shift(1)
        .rolling(window=3, min_periods=3)
        .mean()
    )

    # Filtragem estrita do Período de Teste: Q1 2026 (Jan, Fev, Mar)
    df_teste = df[(df['mes'] >= '2026-01-01') & (df['mes'] <= '2026-03-31')].copy()

    # Arredondamento e cálculo de erro conforme premissa do desafio
    df_teste['previsao_arredondada'] = df_teste['previsao_baseline'].round().astype(int)
    df_teste['erro_absoluto'] = np.abs(df_teste['qtd_real'] - df_teste['previsao_baseline'])

    print("\n" + "="*80)
    print("--- [QUESTÃO 6] PREVISÃO DE DEMANDA - BÚSSOLA DE BORDO 702 (Q1 2026) ---")
    print("="*80)
    print(df_teste[['mes', 'qtd_real', 'previsao_baseline', 'previsao_arredondada', 'erro_absoluto']].to_string(index=False))
    
    soma_previsao_int = df_teste['previsao_arredondada'].sum()
    mae = df_teste['erro_absoluto'].mean()

    print("-" * 80)
    print(f"SOMA TOTAL DA PREVISÃO (Q1 2026): {soma_previsao_int} unidades")
    print(f"MÉTRICA MAE (Mean Absolute Error): {mae:.2f} unidades")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_q6_forecast()