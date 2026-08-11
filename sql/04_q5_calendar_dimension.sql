-- 1. Geração da dimensão de calendário usando a função nativa do DuckDB
WITH dim_calendar AS (
    SELECT CAST(generate_series AS DATE) AS full_date
    FROM generate_series(
        (SELECT MIN(CAST(placed_at AS DATE)) FROM orders),
        (SELECT MAX(CAST(placed_at AS DATE)) FROM orders),
        INTERVAL '1 day'
    )
),

-- 2. Agregação diária das vendas apenas de lojas físicas (channel = 'pos')
daily_pos_sales AS (
    SELECT 
        CAST(placed_at AS DATE) AS sale_date,
        SUM(total) AS total_daily_sales
    FROM orders
    WHERE LOWER(channel) = 'pos'
    GROUP BY CAST(placed_at AS DATE)
),

-- 3. Junção do calendário completo com as vendas diárias (preenchendo dias zerados)
calendar_with_sales AS (
    SELECT 
        c.full_date,
        EXTRACT(DOW FROM c.full_date) AS day_of_week_num,
        CASE EXTRACT(DOW FROM c.full_date)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana,
        COALESCE(s.total_daily_sales, 0.00) AS total_sales
    FROM dim_calendar c
    LEFT JOIN daily_pos_sales s 
        ON c.full_date = s.sale_date
)

-- 4. Cálculo da média real das vendas agrupadas por dia da semana
SELECT 
    dia_semana,
    COUNT(full_date) AS total_dias_no_periodo,
    SUM(total_sales) AS faturamento_total,
    ROUND(AVG(total_sales), 2) AS media_vendas_diaria
FROM calendar_with_sales
GROUP BY day_of_week_num, dia_semana
ORDER BY media_vendas_diaria ASC;