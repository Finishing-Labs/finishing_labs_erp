# Finishing Labs ERP

An Enterprise Resource Planning system for aluminum anodizing operations.

## Tech Stack

- **Frontend**: HTML, Tailwind CSS, HTMX
- **Templating**: Jinja2
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy + SQLite (can be changed to PostgreSQL/MySQL)
- **Architecture**: Model-View-Controller (MVC)

## Project Structure

```
finishing_labs_erp/
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── models/                     # Models (Database layer)
│   ├── __init__.py
│   ├── customer.py
│   ├── order.py
│   ├── inventory.py
│   ├── production.py
│   └── quality_control.py
├── controllers/                # Controllers (Business logic & routes)
│   ├── __init__.py
│   ├── dashboard.py
│   ├── customers.py
│   ├── orders.py
│   ├── inventory.py
│   ├── production.py
│   └── quality_control.py
├── templates/                  # Views (Jinja2 templates)
│   ├── base.html
│   ├── components/            # Reusable components
│   ├── dashboard/
│   ├── customers/
│   ├── orders/
│   ├── inventory/
│   ├── production/
│   └── quality_control/
├── static/                     # Static assets
│   ├── css/
│   ├── js/
│   └── images/
└── utils/                      # Utility functions
    ├── __init__.py
    ├── helpers.py
    └── validators.py
```

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Features

- Dashboard with key metrics
- Customer management
- Order tracking
- Inventory management
- Production job management
- Quality control tracking
