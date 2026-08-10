-- ========================================================
-- SCHEMA DDL GERADO AUTOMATICAMENTE VIA PYTHON NATURO
-- Data de Geração: 2026-08-10 15:40:05
-- PostgreSQL Compatible
-- ========================================================

-- Drop & Create Table para: addresses
DROP TABLE IF EXISTS addresses CASCADE;
CREATE TABLE addresses (
    id VARCHAR(255),
    customer_id VARCHAR(255),
    address_type VARCHAR,
    postal_code VARCHAR(255),
    street VARCHAR,
    number VARCHAR(255),
    complement VARCHAR,
    district VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    is_primary BOOLEAN
);

-- Drop & Create Table para: attributes
DROP TABLE IF EXISTS attributes CASCADE;
CREATE TABLE attributes (
    id VARCHAR(255),
    name VARCHAR,
    data_type VARCHAR
);

-- Drop & Create Table para: brands
DROP TABLE IF EXISTS brands CASCADE;
CREATE TABLE brands (
    id VARCHAR(255),
    name VARCHAR,
    country VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: categories
DROP TABLE IF EXISTS categories CASCADE;
CREATE TABLE categories (
    id VARCHAR(255),
    name VARCHAR,
    slug VARCHAR,
    parent_category_id VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: customers
DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers (
    id VARCHAR(255),
    person_type VARCHAR,
    legal_name VARCHAR,
    trade_name VARCHAR,
    tax_id BIGINT,
    state_registration VARCHAR(255),
    email VARCHAR,
    phone VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: employees
DROP TABLE IF EXISTS employees CASCADE;
CREATE TABLE employees (
    id VARCHAR(255),
    full_name VARCHAR,
    cpf BIGINT,
    email VARCHAR,
    role VARCHAR,
    primary_location_id VARCHAR(255),
    hire_date DATE,
    termination_date DATE,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: fiscal_invoices
DROP TABLE IF EXISTS fiscal_invoices CASCADE;
CREATE TABLE fiscal_invoices (
    id VARCHAR(255),
    order_id VARCHAR(255),
    nfe_number VARCHAR,
    nfe_access_key VARCHAR(255),
    series INTEGER,
    issued_at TIMESTAMP,
    status VARCHAR,
    total_amount NUMERIC(14, 2),
    xml_storage_uri VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: goods_receipt_items
DROP TABLE IF EXISTS goods_receipt_items CASCADE;
CREATE TABLE goods_receipt_items (
    id VARCHAR(255),
    goods_receipt_id VARCHAR(255),
    purchase_order_item_id VARCHAR(255),
    quantity_received VARCHAR(255)
);

-- Drop & Create Table para: goods_receipts
DROP TABLE IF EXISTS goods_receipts CASCADE;
CREATE TABLE goods_receipts (
    id VARCHAR(255),
    purchase_order_id VARCHAR(255),
    received_by_employee_id VARCHAR(255),
    received_at TIMESTAMP,
    notes VARCHAR,
    created_at TIMESTAMP
);

-- Drop & Create Table para: locations
DROP TABLE IF EXISTS locations CASCADE;
CREATE TABLE locations (
    id VARCHAR(255),
    name VARCHAR,
    location_type VARCHAR,
    postal_code VARCHAR(255),
    street VARCHAR,
    number INTEGER,
    complement VARCHAR,
    district VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: order_items
DROP TABLE IF EXISTS order_items CASCADE;
CREATE TABLE order_items (
    id VARCHAR(255),
    order_id VARCHAR(255),
    product_variant_id VARCHAR(255),
    quantity VARCHAR(255),
    unit_price NUMERIC(14, 2),
    icms_rate NUMERIC(14, 2),
    ipi_rate NUMERIC(14, 2),
    line_total NUMERIC(14, 2)
);

-- Drop & Create Table para: orders
DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
    id VARCHAR(255),
    order_number VARCHAR,
    channel VARCHAR,
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id VARCHAR(255),
    status VARCHAR,
    subtotal NUMERIC(14, 2),
    discount_amount NUMERIC(14, 2),
    total NUMERIC(14, 2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: payments
DROP TABLE IF EXISTS payments CASCADE;
CREATE TABLE payments (
    id VARCHAR(255),
    order_id VARCHAR(255),
    method VARCHAR,
    installments VARCHAR(255),
    amount NUMERIC(14, 2),
    status VARCHAR,
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: product_suppliers
DROP TABLE IF EXISTS product_suppliers CASCADE;
CREATE TABLE product_suppliers (
    product_variant_id VARCHAR(255),
    supplier_id VARCHAR(255),
    supplier_sku VARCHAR,
    last_quoted_cost NUMERIC(14, 2),
    lead_time_days INTEGER,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: product_variants
DROP TABLE IF EXISTS product_variants CASCADE;
CREATE TABLE product_variants (
    id VARCHAR(255),
    product_id VARCHAR(255),
    sku VARCHAR,
    barcode_ean BIGINT,
    sale_price NUMERIC(14, 2),
    cost_price NUMERIC(14, 2),
    weight_kg NUMERIC(14, 2),
    icms_rate NUMERIC(14, 2),
    ipi_rate NUMERIC(14, 2),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: products
DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products (
    id VARCHAR(255),
    name VARCHAR,
    description VARCHAR,
    brand_id VARCHAR(255),
    category_id VARCHAR(255),
    ncm_code INTEGER,
    unit_of_measure VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: purchase_order_items
DROP TABLE IF EXISTS purchase_order_items CASCADE;
CREATE TABLE purchase_order_items (
    id VARCHAR(255),
    purchase_order_id VARCHAR(255),
    product_variant_id VARCHAR(255),
    quantity_ordered VARCHAR(255),
    unit_cost NUMERIC(14, 2),
    line_total NUMERIC(14, 2)
);

-- Drop & Create Table para: purchase_orders
DROP TABLE IF EXISTS purchase_orders CASCADE;
CREATE TABLE purchase_orders (
    id VARCHAR(255),
    po_number VARCHAR,
    supplier_id VARCHAR(255),
    buyer_id INTEGER,
    destination_location_id VARCHAR(255),
    status VARCHAR,
    currency VARCHAR,
    subtotal NUMERIC(14, 2),
    total NUMERIC(14, 2),
    placed_at TIMESTAMP,
    expected_delivery_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: return_items
DROP TABLE IF EXISTS return_items CASCADE;
CREATE TABLE return_items (
    id VARCHAR(255),
    return_id VARCHAR(255),
    order_item_id INTEGER,
    quantity VARCHAR(255),
    action VARCHAR,
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(14, 2)
);

-- Drop & Create Table para: returns
DROP TABLE IF EXISTS returns CASCADE;
CREATE TABLE returns (
    id VARCHAR(255),
    return_number VARCHAR,
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id VARCHAR(255),
    status VARCHAR,
    reason VARCHAR,
    total_refund_amount NUMERIC(14, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: stock_levels
DROP TABLE IF EXISTS stock_levels CASCADE;
CREATE TABLE stock_levels (
    product_variant_id VARCHAR(255),
    location_id VARCHAR(255),
    quantity_on_hand NUMERIC(14, 2),
    reorder_point VARCHAR(255),
    updated_at TIMESTAMP
);

-- Drop & Create Table para: stock_movements
DROP TABLE IF EXISTS stock_movements CASCADE;
CREATE TABLE stock_movements (
    id VARCHAR(255),
    product_variant_id VARCHAR(255),
    location_id VARCHAR(255),
    movement_type VARCHAR,
    quantity NUMERIC(14, 2),
    reference_table VARCHAR(255),
    reference_id VARCHAR(255),
    employee_id VARCHAR(255),
    notes VARCHAR,
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

-- Drop & Create Table para: suppliers
DROP TABLE IF EXISTS suppliers CASCADE;
CREATE TABLE suppliers (
    id VARCHAR(255),
    legal_name VARCHAR,
    trade_name VARCHAR,
    country VARCHAR,
    tax_id VARCHAR(255),
    tax_id_type VARCHAR,
    email VARCHAR,
    phone BIGINT,
    contact_name VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Drop & Create Table para: variant_attribute_values
DROP TABLE IF EXISTS variant_attribute_values CASCADE;
CREATE TABLE variant_attribute_values (
    product_variant_id VARCHAR(255),
    attribute_id VARCHAR(255),
    value VARCHAR(255)
);

