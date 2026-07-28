--------------------------------------------------
-- Total Sales
--------------------------------------------------

SELECT SUM(sales) AS total_sales
FROM sales;

--------------------------------------------------
-- Average Sales
--------------------------------------------------

SELECT ROUND(AVG(sales),2) AS average_sales
FROM sales;

--------------------------------------------------
-- Total Orders
--------------------------------------------------

SELECT COUNT(*) AS total_orders
FROM sales;

--------------------------------------------------
-- Best Selling Category
--------------------------------------------------

SELECT category,
       SUM(sales) AS total_sales
FROM sales
GROUP BY category
ORDER BY total_sales DESC;

--------------------------------------------------
-- Region-wise Sales
--------------------------------------------------

SELECT region,
       SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

--------------------------------------------------
-- Monthly Sales Trend
--------------------------------------------------

SELECT
strftime('%Y-%m',order_date) AS month,
SUM(sales) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month;

--------------------------------------------------
-- Top 5 Products
--------------------------------------------------

SELECT
product_name,
SUM(sales) AS revenue
FROM sales
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 5;

--------------------------------------------------
-- Sales by Sub Category
--------------------------------------------------

SELECT
sub_category,
SUM(sales) AS total_sales
FROM sales
GROUP BY sub_category
ORDER BY total_sales DESC;

--------------------------------------------------
-- Orders Greater Than $500
--------------------------------------------------

SELECT *
FROM sales
WHERE sales > 500;

--------------------------------------------------
-- Update Example
--------------------------------------------------

UPDATE sales
SET sales = 1900
WHERE order_id = 1;

--------------------------------------------------
-- Delete Example
--------------------------------------------------

DELETE FROM sales
WHERE order_id = 8;