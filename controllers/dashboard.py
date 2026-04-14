"""
Dashboard Controller - Homepage and overview metrics

HOW THIS CONTROLLER WORKS:
1. Creates a Flask blueprint (mini-app) for dashboard routes
2. Defines route handlers (functions that respond to URL requests)
3. Checks if request is from HTMX or regular browser
4. Returns either partial content (HTMX) or full page (regular)
"""
from flask import Blueprint, render_template, request

# Create blueprint - groups related routes together
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():

    return render_template('dashboard/content.html', page_title='Dashboard')

