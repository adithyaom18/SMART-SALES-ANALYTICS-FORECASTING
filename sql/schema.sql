-- Create Sales Table

CREATE TABLE sales (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date DATE NOT NULL,
    customer_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT,
    region TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    sales REAL NOT NULL
);