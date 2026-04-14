"""
Finishing Labs ERP - Main Application Entry Point

This Flask application uses:
- Jinja2 templating for dynamic HTML rendering
- HTMX for seamless navigation without full page reloads
- SQLAlchemy for database management
- Blueprint pattern for modular controllers
"""
from flask import Flask, request
from config import Config
from models import db
from controllers import register_blueprints


def create_app(config_class=Config):
    """
    Application Factory Pattern
    
    Creates and configures the Flask application instance.
    This pattern allows multiple app instances with different configs (dev, test, prod).
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize SQLAlchemy database connection
    db.init_app(app)
    
    # Register all blueprints (controllers) for different sections
    register_blueprints(app)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Helper function to detect HTMX requests
    # HTMX sends a special header "HX-Request: true" with every AJAX call
    @app.context_processor
    def utility_processor():
        """
        Makes helper functions available in all Jinja2 templates
        
        is_htmx: Returns True if request came from HTMX (partial update)
        """
        return dict(
            is_htmx=lambda: request.headers.get('HX-Request') == 'true'
        )
    
    return app


if __name__ == '__main__':
    app = create_app()
    # debug=True enables hot reload and detailed error pages
    app.run(debug=True, host='127.0.0.1', port=5000)
