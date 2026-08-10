-- Questão 3.2: Soma total de linhas das tabelas solicitadas
SELECT 
    (SELECT COUNT(*) FROM customers) AS qtd_customers,
    (SELECT COUNT(*) FROM orders) AS qtd_orders,
    (SELECT COUNT(*) FROM order_items) AS qtd_order_items,
    (SELECT COUNT(*) FROM payments) AS qtd_payments,
    (
        (SELECT COUNT(*) FROM customers) + 
        (SELECT COUNT(*) FROM orders) + 
        (SELECT COUNT(*) FROM order_items) + 
        (SELECT COUNT(*) FROM payments)
    ) AS total_linhas_somadas;