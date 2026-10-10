-- Day 5: Data Warehouse Fundamentals
-- Schema: Star schema for sales analysis

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50)
);

CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    brand VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    quarter INT,
    year INT
);

CREATE TABLE fact_sales (
    order_id INT,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    date_id INT REFERENCES dim_date(date_id),
    quantity INT,
    unit_price INT,
    total_amount INT,
    PRIMARY KEY (order_id, product_id)
);

-- 1. Total sales by city
SELECT dc.city,
       SUM(fs.total_amount) AS total_sales
FROM dim_customer dc
JOIN fact_sales fs
    ON dc.customer_id = fs.customer_id
GROUP BY dc.city
ORDER BY total_sales DESC;


-- 2. Total sales by product category
SELECT dp.category,
       SUM(fs.total_amount) AS total_sales
FROM dim_product dp
JOIN fact_sales fs
    ON dp.product_id = fs.product_id
GROUP BY dp.category
ORDER BY total_sales DESC;


-- 3. Top-selling products by revenue
SELECT dp.product_name,
       SUM(fs.total_amount) AS total_sales
FROM dim_product dp
JOIN fact_sales fs
    ON dp.product_id = fs.product_id
GROUP BY dp.product_name
ORDER BY total_sales DESC;


-- 4. Customer total spending
SELECT dc.customer_id,
       dc.name,
       SUM(fs.total_amount) AS total_spending
FROM dim_customer dc
JOIN fact_sales fs
    ON dc.customer_id = fs.customer_id
GROUP BY dc.customer_id, dc.name
ORDER BY total_spending DESC;


-- 5. Daily sales
SELECT dd.full_date,
       SUM(fs.total_amount) AS total_sales
FROM dim_date dd
JOIN fact_sales fs
    ON dd.date_id = fs.date_id
GROUP BY dd.full_date
ORDER BY dd.full_date;


-- 6. Order count and sales by city
SELECT dc.city,
       SUM(fs.total_amount) AS total_sales,
       COUNT(DISTINCT fs.order_id) AS order_count
FROM dim_customer dc
JOIN fact_sales fs
    ON dc.customer_id = fs.customer_id
GROUP BY dc.city
ORDER BY total_sales DESC;