-- ============================================================================
-- CAMADA GOLD - MODELAGEM DIMENSIONAL PARA POWER BI (CHAVES ÚNICAS)
-- ============================================================================

-- 1. DIMENSÃO CALENDÁRIO
CREATE OR REPLACE TABLE gold_dim_calendario AS
WITH dim_calendar AS (
    SELECT CAST(generate_series AS DATE) AS full_date
    FROM generate_series(
        (SELECT MIN(CAST(placed_at AS DATE)) FROM orders),
        (SELECT MAX(CAST(placed_at AS DATE)) FROM orders),
        INTERVAL '1 day'
    )
)
SELECT 
    full_date AS data,
    EXTRACT(YEAR FROM full_date) AS ano,
    EXTRACT(MONTH FROM full_date) AS mes,
    EXTRACT(DAY FROM full_date) AS dia,
    EXTRACT(DOW FROM full_date) AS day_of_week_num,
    CASE EXTRACT(DOW FROM full_date)
        WHEN 0 THEN 'Domingo'
        WHEN 1 THEN 'Segunda-feira'
        WHEN 2 THEN 'Terça-feira'
        WHEN 3 THEN 'Quarta-feira'
        WHEN 4 THEN 'Quinta-feira'
        WHEN 5 THEN 'Sexta-feira'
        WHEN 6 THEN 'Sábado'
    END AS dia_semana,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0, 6) THEN TRUE ELSE FALSE END AS is_final_semana,
    STRFTIME(full_date, '%Y-%m') AS ano_mes
FROM dim_calendar;

-- 2. DIMENSÃO PRODUTOS (Chave única por variante)
CREATE OR REPLACE TABLE gold_dim_produtos AS
SELECT 
    pv.id AS variant_id,
    p.id AS product_id,
    p.name AS product_name,
    c.name AS category_name,
    pv.sku,
    COALESCE(pv.sale_price, 0.00) AS preco_tabela,
    COALESCE(pv.cost_price, 0.00) AS custo_padrao
FROM product_variants pv
LEFT JOIN products p ON pv.product_id = p.id
LEFT JOIN categories c ON p.category_id = c.id;

-- 3. DIMENSÃO CLIENTES (Garante chave única por cliente)
CREATE OR REPLACE TABLE gold_dim_clientes AS
SELECT 
    c.id AS customer_id,
    COALESCE(c.legal_name, c.trade_name, 'Cliente ' || c.id) AS nome_cliente,
    c.email,
    c.created_at AS data_cadastro
FROM customers c;

-- 4. TABELA FATO DE VENDAS
CREATE OR REPLACE TABLE gold_fato_vendas AS
SELECT 
    oi.id AS order_item_id,
    o.id AS order_id,
    o.customer_id,
    pv.product_id,
    oi.product_variant_id AS variant_id, -- Nomeado exatamente igual à dimensão de produtos
    CAST(o.placed_at AS DATE) AS data_pedido,
    LOWER(o.channel) AS canal,
    LOWER(o.status) AS status_pedido,
    CAST(oi.quantity AS INTEGER) AS quantidade,
    CAST(oi.unit_price AS DECIMAL(14,2)) AS preco_unitario,
    (CAST(oi.quantity AS INTEGER) * CAST(oi.unit_price AS DECIMAL(14,2))) AS faturamento_bruto,
    (CAST(oi.quantity AS INTEGER) * CAST(oi.unit_price AS DECIMAL(14,2))) - 
    (CAST(oi.quantity AS INTEGER) * COALESCE(pv.cost_price, 0.00)) AS lucro_estimado
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN product_variants pv ON oi.product_variant_id = pv.id;