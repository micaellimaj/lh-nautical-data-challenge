-- QUERY 1: Top 10 Clientes de Elite
WITH customer_metrics AS (
    SELECT 
        o.customer_id,
        COUNT(DISTINCT o.id) AS frequencia,
        SUM(o.total) AS faturamento_total,
        (SUM(o.total) / COUNT(DISTINCT o.id)) AS ticket_medio,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
)
SELECT 
    cm.customer_id,
    c.legal_name AS nome_cliente,
    cm.frequencia,
    ROUND(cm.faturamento_total, 2) AS faturamento_total,
    ROUND(cm.ticket_medio, 2) AS ticket_medio,
    cm.diversidade_categorias
FROM customer_metrics cm
JOIN customers c ON cm.customer_id = c.id
ORDER BY cm.ticket_medio DESC, cm.customer_id ASC
LIMIT 10;

-- QUERY 2: Categoria Líder de Consumo entre os Top 10 Clientes
WITH customer_metrics AS (
    SELECT 
        o.customer_id,
        SUM(o.total) / COUNT(DISTINCT o.id) AS ticket_medio,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
),
top_10_elite AS (
    SELECT customer_id
    FROM customer_metrics
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10
)
SELECT 
    cat.id AS category_id,
    cat.name AS nome_categoria,
    SUM(CAST(oi.quantity AS INTEGER)) AS total_itens_comprados
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN product_variants pv ON oi.product_variant_id = pv.id
JOIN products p ON pv.product_id = p.id
JOIN categories cat ON p.category_id = cat.id
WHERE o.customer_id IN (SELECT customer_id FROM top_10_elite)
GROUP BY cat.id, cat.name
ORDER BY total_itens_comprados DESC
LIMIT 1;