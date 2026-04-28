"""
Customer Service - Business logic and data access for customers

All customer-related SQL queries and business logic.
Controllers call these functions to keep controllers thin.
"""

from database.db import DB


def get_all_customers(active_only=True):
    \"\"\"Get list of all customers\"\"\"
    if active_only:
        sql = """
            SELECT customer_id, company_name, contact_email, phone, active, created_at
            FROM customers
            WHERE active = %s
            ORDER BY company_name
        """
        return DB.query(sql, [True])
    else:
        sql = """
            SELECT customer_id, company_name, contact_email, phone, active, created_at
            FROM customers
            ORDER BY company_name
        """
        return DB.query(sql)


def get_customer_by_id(customer_id):
    """Get single customer by ID"""
    sql = """
        SELECT customer_id, company_name, contact_email, phone, 
               address, city, state, zip_code, active, created_at
        FROM customers
        WHERE customer_id = %s
    """
    return DB.fetch_one(sql, [customer_id])


def search_customers(search_term):
    """Search customers by name or email"""
    sql = """
        SELECT customer_id, company_name, contact_email, phone
        FROM customers
        WHERE company_name ILIKE %s OR contact_email ILIKE %s
        ORDER BY company_name
    """
    search_pattern = f"%{search_term}%"
    return DB.query(sql, [search_pattern, search_pattern])


def create_customer(company_name, contact_email, phone=None, address=None, 
                   city=None, state=None, zip_code=None):
    """Create new customer, return generated ID"""
    sql = """
        INSERT INTO customers (
            company_name, contact_email, phone, 
            address, city, state, zip_code, active, created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        RETURNING customer_id
    """
    return DB.execute_returning_id(sql, [
        company_name, contact_email, phone,
        address, city, state, zip_code, True
    ])


def update_customer(customer_id, company_name=None, contact_email=None, 
                   phone=None, address=None, city=None, state=None, zip_code=None):
    """Update existing customer, return affected row count"""
    # Build dynamic UPDATE query based on provided fields
    updates = []
    params = []
    
    if company_name is not None:
        updates.append("company_name = %s")
        params.append(company_name)
    
    if contact_email is not None:
        updates.append("contact_email = %s")
        params.append(contact_email)
    
    if phone is not None:
        updates.append("phone = %s")
        params.append(phone)
    
    if address is not None:
        updates.append("address = %s")
        params.append(address)
    
    if city is not None:
        updates.append("city = %s")
        params.append(city)
    
    if state is not None:
        updates.append("state = %s")
        params.append(state)
    
    if zip_code is not None:
        updates.append("zip_code = %s")
        params.append(zip_code)
    
    if not updates:
        return 0
    
    params.append(customer_id)
    sql = f"""
        UPDATE customers
        SET {', '.join(updates)}
        WHERE customer_id = %s
    """
    
    return DB.execute(sql, params)


def deactivate_customer(customer_id):
    """Deactivate customer (soft delete)"""
    sql = """
        UPDATE customers
        SET active = %s
        WHERE customer_id = %s
    """
    return DB.execute(sql, [False, customer_id])


def get_customer_stats(customer_id):
    """Get statistics for a customer (order count, revenue, etc.)"""
    sql = """
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            COUNT(DISTINCT o.order_id) FILTER (WHERE o.status = 'active') as active_orders
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE c.customer_id = %s
        GROUP BY c.customer_id
    """
    return DB.fetch_one(sql, [customer_id])


def validate_customer_data(company_name, contact_email):
    """Validate customer data, return (is_valid, error_list)"""
    errors = []
    
    if not company_name or len(company_name.strip()) < 2:
        errors.append("Company name must be at least 2 characters")
    
    if not contact_email or '@' not in contact_email:
        errors.append("Valid email address required")
    
    existing = DB.fetch_one(
        "SELECT customer_id FROM customers WHERE contact_email = %s",
        [contact_email]
    )
    if existing:
        errors.append("Email address already exists")
    
    return (len(errors) == 0, errors)
