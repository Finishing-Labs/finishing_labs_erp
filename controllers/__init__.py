"""
Controllers Package - Registers Flask blueprints

Each controller handles HTTP routing for a section of the app.
"""

def register_blueprints(app):
    """Register all Flask blueprints with app"""
    
    from .dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    from .purchase_orders import purchase_orders_bp
    app.register_blueprint(purchase_orders_bp, url_prefix='/purchase-orders')
    
    from .work_orders import work_orders_bp
    app.register_blueprint(work_orders_bp, url_prefix='/work-orders')
    
    from .packing_slips import packing_slips_bp
    app.register_blueprint(packing_slips_bp, url_prefix='/packing-slips')
    
    from .customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')
