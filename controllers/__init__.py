"""
Controllers Package - Registers all Flask blueprints

This __init__.py makes it easy to import and register all controllers at once.
Each controller (blueprint) handles a specific section of the application.
"""

def register_blueprints(app):
    """
    Register all Flask blueprints with the app
    
    WHAT ARE BLUEPRINTS?
    - Blueprints are modular components that group related routes
    - Think of them as mini-applications
    - Helps organize code by feature (purchase_orders, customers, work_orders, etc.)
    
    HOW IT WORKS:
    - Import each blueprint from its module
    - Register it with app.register_blueprint()
    - URL prefix organizes routes (e.g., /purchase-orders/list, /purchase-orders/create)
    """
    
    # Dashboard blueprint - Homepage and overview
    from .dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    # Purchase Orders blueprint - Purchase order management
    from .purchase_orders import purchase_orders_bp
    app.register_blueprint(purchase_orders_bp, url_prefix='/purchase-orders')
    
    # Work Orders blueprint - Work order tracking
    from .work_orders import work_orders_bp
    app.register_blueprint(work_orders_bp, url_prefix='/work-orders')
    
    # Packing Slips blueprint - Packing slip creation and management
    from .packing_slips import packing_slips_bp
    app.register_blueprint(packing_slips_bp, url_prefix='/packing-slips')
    
    # Customers blueprint - Customer management
    from .customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')
