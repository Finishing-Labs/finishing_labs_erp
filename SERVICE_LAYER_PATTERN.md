# Service Layer Pattern - Architecture Guide

## 🎯 Pattern Overview

This project uses the **Service Layer Pattern** (also called Repository Pattern):

```
Templates (HTMX) → Controllers → Services → Database → PostgreSQL
```

### Why This Pattern?

✅ **Separation of concerns** - Each layer has one job  
✅ **Testable** - Business logic testable without HTTP  
✅ **Reusable** - Multiple controllers can use same services  
✅ **Maintainable** - Changes happen in predictable places  
✅ **No ORM** - Full SQL control, write queries your way  

## 📂 Directory Structure

```
finishing_labs_erp/
├── controllers/          # HTTP routing (thin)
│   ├── customers.py      # Routes: /customers, /customers/create, etc.
│   ├── purchase_orders.py
│   └── work_orders.py
│
├── services/             # Business logic + SQL (thick)
│   ├── customer_service.py       # All customer SQL queries
│   ├── purchase_order_service.py
│   └── work_order_service.py
│
├── database/             # DB utility
│   └── db.py            # DB.query(), DB.execute(), etc.
│
└── templates/            # Views
    └── customers/
        ├── content.html
        └── create_content.html
```

## 🔄 Request Flow Example

**User clicks "New Customer" button:**

```
1. HTMX: GET /customers/create
   ↓
2. Controller (customers.py):
   @customers_bp.route('/create')
   def create():
       return render_template('customers/create_content.html')
   ↓
3. User fills form, clicks "Create"
   ↓
4. HTMX: POST /customers with form data
   ↓
5. Controller:
   @customers_bp.route('/', methods=['POST'])
   def store():
       # Get form data
       name = request.form.get('company_name')
       email = request.form.get('contact_email')
       
       # Call service (no SQL here!)
       customer_id = customer_service.create_customer(name, email)
       
       # Return success view
       return render_template('customers/content.html', success=True)
   ↓
6. Service (customer_service.py):
   def create_customer(name, email):
       sql = "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id"
       return DB.execute_returning_id(sql, [name, email])
   ↓
7. DB Utility (db.py):
   Executes SQL with psycopg2, returns result
   ↓
8. PostgreSQL: Data inserted, ID returned
```

## 🧩 Each Layer's Job

### Templates (Views)
- Display HTML/data
- Capture user input
- Send HTMX requests

**Don't:** Put business logic or SQL in templates

### Controllers (HTTP Layer)
- Handle routing
- Get request data (form, query params)
- Call service functions
- Return appropriate template

**Don't:** Write SQL or complex logic in controllers

### Services (Business Logic + Data Access)
- Validate data
- Execute SQL queries
- Business rules
- Return clean data structures

**Don't:** Handle HTTP requests directly

### Database Utility
- Execute SQL safely (parameterized queries)
- Manage connections
- Transaction support

## 📖 Usage Examples

### Simple Query

**Controller:**
```python
from services import customer_service

@customers_bp.route('/')
def index():
    customers = customer_service.get_all_customers()
    return render_template('customers/content.html', customers=customers)
```

**Service:**
```python
from database.db import DB

def get_all_customers():
    sql = "SELECT * FROM customers WHERE active = %s ORDER BY company_name"
    return DB.query(sql, [True])
```

### Creating Records

**Controller:**
```python
@customers_bp.route('/', methods=['POST'])
def store():
    name = request.form.get('company_name')
    email = request.form.get('contact_email')
    
    # Validate
    valid, errors = customer_service.validate_customer_data(name, email)
    if not valid:
        return render_template('customers/create_content.html', errors=errors)
    
    # Create
    customer_id = customer_service.create_customer(name, email)
    
    # Success
    customers = customer_service.get_all_customers()
    return render_template('customers/content.html', 
                         customers=customers,
                         success='Customer created!')
```

**Service:**
```python
def create_customer(name, email, phone=None):
    sql = """
        INSERT INTO customers (company_name, contact_email, phone, created_at)
        VALUES (%s, %s, %s, NOW())
        RETURNING customer_id
    """
    return DB.execute_returning_id(sql, [name, email, phone])

def validate_customer_data(name, email):
    errors = []
    if not name or len(name) < 2:
        errors.append("Name must be at least 2 characters")
    if not email or '@' not in email:
        errors.append("Valid email required")
    return (len(errors) == 0, errors)
```

### Transactions (Multi-Step Operations)

**Service:**
```python
from database.db import DB

def create_order_with_items(customer_id, items):
    """
    Create order and multiple order items in one transaction
    """
    with DB.transaction():
        # Create order
        order_id = DB.execute_returning_id(
            "INSERT INTO orders (customer_id, created_at) VALUES (%s, NOW()) RETURNING order_id",
            [customer_id]
        )
        
        # Add all items
        for item in items:
            DB.execute(
                "INSERT INTO order_items (order_id, product, qty) VALUES (%s, %s, %s)",
                [order_id, item['product'], item['qty']]
            )
        
        return order_id
    # If any query fails, everything rolls back automatically
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

**Local Development (.env file):**
```
DB_NAME=finishing_labs_erp
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

**Production (Render):**
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### 3. Create Database Schema

Run your SQL schema file:
```bash
psql -U postgres -d finishing_labs_erp -f schema.sql
```

### 4. Use in Your Code

**Controller:**
```python
from services import customer_service

@customers_bp.route('/')
def index():
    customers = customer_service.get_all_customers()
    return render_template('customers/content.html', customers=customers)
```

## 🎨 Design Principles

### 1. Controllers Stay Thin
Controllers should be ~10-20 lines max:
- Get request data
- Call 1-2 service functions  
- Return template

### 2. Services Are Domain-Focused
One service file per domain:
- `customer_service.py` - all customer operations
- `purchase_order_service.py` - all PO operations
- Keep related SQL together

### 3. Write SQL, Don't Generate It
You write the queries:
```python
sql = """
    SELECT c.*, COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.active = %s
    GROUP BY c.customer_id
    ORDER BY order_count DESC
"""
```

### 4. Use Parameterized Queries Always
**Never:**
```python
sql = f"SELECT * FROM customers WHERE id = {customer_id}"  # SQL INJECTION!
```

**Always:**
```python
sql = "SELECT * FROM customers WHERE id = %s"
result = DB.fetch_one(sql, [customer_id])  # Safe!
```

## 🧪 Testing

Services are easy to test:

```python
def test_create_customer():
    customer_id = customer_service.create_customer(
        company_name='Test Corp',
        contact_email='test@example.com'
    )
    assert customer_id is not None
    
    customer = customer_service.get_customer_by_id(customer_id)
    assert customer['company_name'] == 'Test Corp'
```

## 🔧 Common Patterns

### Pattern: List with Search
```python
def get_customers(search_term=None, active_only=True):
    if search_term:
        sql = """
            SELECT * FROM customers 
            WHERE (company_name ILIKE %s OR contact_email ILIKE %s)
            AND active = %s
        """
        pattern = f"%{search_term}%"
        return DB.query(sql, [pattern, pattern, active_only])
    else:
        sql = "SELECT * FROM customers WHERE active = %s"
        return DB.query(sql, [active_only])
```

### Pattern: Get with Stats
```python
def get_customer_with_order_stats(customer_id):
    sql = """
        SELECT 
            c.*,
            COUNT(o.order_id) as total_orders,
            SUM(o.amount) as total_revenue
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE c.customer_id = %s
        GROUP BY c.customer_id
    """
    return DB.fetch_one(sql, [customer_id])
```

### Pattern: Conditional Update
```python
def update_customer(customer_id, **updates):
    """Update only provided fields"""
    if not updates:
        return 0
    
    set_clauses = []
    params = []
    
    for field, value in updates.items():
        set_clauses.append(f"{field} = %s")
        params.append(value)
    
    params.append(customer_id)
    
    sql = f"""
        UPDATE customers 
        SET {', '.join(set_clauses)}
        WHERE customer_id = %s
    """
    return DB.execute(sql, params)
```

## 📚 Learn More

- See `controllers/EXAMPLE_customers_with_service_layer.py` for complete working example
- See `services/customer_service.py` for all query patterns
- See `database/db.py` for DB utility documentation

## ❓ FAQ

**Q: Why not use SQLAlchemy ORM?**  
A: Full control over SQL, simpler mental model, easier debugging, better for complex ERP queries.

**Q: Where do validations go?**  
A: In service functions. Keep them close to the data logic.

**Q: Can I call one service from another?**  
A: Yes! Services can call other services. Keep business logic in services.

**Q: How do I handle errors?**  
A: Let database errors bubble up to controllers, handle them there with user-friendly messages.

**Q: What about migrations?**  
A: Use SQL files in `migrations/` folder. No ORM = no auto-migrations, but you have full control.
