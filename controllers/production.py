"""
Production Controller - Work order management

Handles:
- Listing all work orders
- Work order builder (creating batches from PO line items)
- Tracking work order progress
"""
from flask import Blueprint, render_template, request

# Create blueprint for production/work order routes
production_bp = Blueprint('production', __name__)


@production_bp.route('/')
def index():
    """
    Work orders list
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('production/content.html', page_title='Work Orders')
    return render_template('production/index.html', page_title='Work Orders')



@production_bp.route('/builder')
def builder():
    """
    Work order builder interface
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('production/builder_content.html', page_title='Work Order Builder')
    return render_template('production/builder.html', page_title='Work Order Builder')



@production_bp.route('/<int:wo_id>')
def view(wo_id):
    """
    View single work order details
    

    """

    
   
    return render_template('production/view_content.html',
                             page_title=f'Work Order {wo_id}',
                             wo_id=wo_id)

