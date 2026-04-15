"""
Packing Slips Controller - Packing slip management

Handles:
- Listing all packing slips
- Creating new packing slips
- Viewing packing slip details
- Printing/exporting packing slips
"""
from flask import Blueprint, render_template, request

# Create blueprint for packing slip routes
packing_slips_bp = Blueprint('packing_slips', __name__)


@packing_slips_bp.route('/')
def index():
    """
    Packing slips list
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('packing_slips/content.html', page_title='Packing Slips')
    return render_template('packing_slips/index.html', page_title='Packing Slips')


@packing_slips_bp.route('/create')
def create():
    """
    Create new packing slip
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('packing_slips/create_content.html', page_title='New Packing Slip')
    return render_template('packing_slips/create.html', page_title='New Packing Slip')


@packing_slips_bp.route('/<int:slip_id>')
def view(slip_id):
    """
    View single packing slip details
    """
    return render_template('packing_slips/view_content.html',
                         page_title=f'Packing Slip #{slip_id}',
                         slip_id=slip_id)
