CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE purchase_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_number VARCHAR(50) UNIQUE,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE work_orders (
    work_order_id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER REFERENCES purchase_orders(order_id),
    work_order_number VARCHAR(50) UNIQUE,
    status VARCHAR(50) DEFAULT 'pending',
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE packing_slips (
    packing_slip_id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER REFERENCES purchase_orders(order_id),
    slip_number VARCHAR(50) UNIQUE,
    shipped_date DATE,
    tracking_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE line_items (
    line_item_id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER REFERENCES purchase_orders(order_id),
    work_order_id INTEGER REFERENCES work_orders(work_order_id),
    packing_slip_id INTEGER REFERENCES packing_slips(packing_slip_id),
    product_name VARCHAR(255),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Add indexes for common queries
CREATE INDEX idx_customers_active ON customers(active);
CREATE INDEX idx_purchase_orders_customer ON purchase_orders(customer_id);
CREATE INDEX idx_line_items_purchase_order ON line_items(purchase_order_id);
CREATE INDEX idx_line_items_work_order ON line_items(work_order_id);
CREATE INDEX idx_line_items_packing_slip ON line_items(packing_slip_id);
CREATE INDEX idx_work_orders_order ON work_orders(purchase_order_id);
CREATE INDEX idx_packing_slips_order ON packing_slips(purchase_order_id);