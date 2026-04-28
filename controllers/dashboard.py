"""
Dashboard Controller
"""
from flask import Blueprint, render_template, request

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    """Dashboard homepage"""
    if request.headers.get('HX-Request'):
        return render_template('dashboard/content.html', page_title='Dashboard')
    return render_template('dashboard/index.html', page_title='Dashboard')

