"""
Finishing Labs ERP - Application Entry Point

Flask app with HTMX for seamless navigation.
"""
from flask import Flask, request
from config import Config
from database import init_db, close_db
from controllers import register_blueprints


def create_app(config_class=Config):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    init_db(app)
    register_blueprints(app)
    
    @app.context_processor
    def utility_processor():
        """Make is_htmx() available in all templates"""
        return dict(
            is_htmx=lambda: request.headers.get('HX-Request') == 'true'
        )
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db(exception)
    
    return app


if __name__ == '__main__':
    app = create_app()
    # debug=True enables hot reload and detailed error pages
    app.run(debug=True, host='127.0.0.1', port=5000)
