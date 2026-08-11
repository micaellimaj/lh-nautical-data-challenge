import duckdb
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Configuração de caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "silver" / "lh_nautical.duckdb"

def run_q7_recommendation():
    con = duckdb.connect(str(DB_PATH))

    # 1. Extração do histórico de compras (Cliente x Produto)
    query = """
    SELECT DISTINCT
        o.customer_id,
        p.id AS product_id,
        p.name AS product_name
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    WHERE o.customer_id IS NOT NULL
      AND LOWER(o.status) NOT IN ('cancelled', 'canceled');
    """
    df_interactions = con.execute(query).df()
    con.close()

    # 2. Construção da Matriz de Interação Usuário x Produto (0 ou 1)
    user_item_matrix = pd.crosstab(
        df_interactions['customer_id'], 
        df_interactions['product_name']
    )
    # Garante a representação binária (1 se comprou, 0 caso contrário)
    user_item_matrix = (user_item_matrix > 0).astype(int)

    # 3. Identificação do produto de referência ("Motor de Popa 1949")
    target_product = None
    for col in user_item_matrix.columns:
        if 'motor de popa 1949' in col.lower():
            target_product = col
            break

    if not target_product:
        raise ValueError("Produto 'Motor de Popa 1949' não encontrado na base de dados.")

    # 4. Cálculo da Similaridade de Cosseno entre Produtos (Produto x Produto)
    # Transpomos a matriz para ter Produtos nas linhas e Clientes nas colunas
    product_vectors = user_item_matrix.T
    similarity_matrix = cosine_similarity(product_vectors)

    # Convertendo para DataFrame para facilitar o ranking
    df_similarity = pd.DataFrame(
        similarity_matrix, 
        index=product_vectors.index, 
        columns=product_vectors.index
    )

    # 5. Ranking dos 5 produtos mais similares ao "Motor de Popa 1949"
    # Remove o próprio produto da lista de recomendações
    similar_scores = df_similarity[target_product].drop(index=target_product)
    top_5_recommendations = similar_scores.sort_values(ascending=False).head(5).reset_index()
    top_5_recommendations.columns = ['Produto Recomendado', 'Score Similaridade (Cosseno)']

    # Exibição dos Resultados no Terminal
    print("\n" + "="*80)
    print(f"--- [QUESTÃO 7] SISTEMA DE RECOMENDAÇÃO: {target_product.upper()} ---")
    print("="*80)
    print(top_5_recommendations.to_string(index=False))
    print("="*80 + "\n")

    # Produto top 1 com maior similaridade
    top_1_product = top_5_recommendations.iloc[0]['Produto Recomendado']
    top_1_score = top_5_recommendations.iloc[0]['Score Similaridade (Cosseno)']
    print(f"PRODUTO COM MAIOR SIMILARIDADE: {top_1_product} (Score: {top_1_score:.4f})\n")

if __name__ == "__main__":
    run_q7_recommendation()