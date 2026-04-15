"""
Orders Controller - Purchase order management

Handles:
- Listing all purchase orders
- Creating new purchase orders
- Viewing order details
- Editing existing orders
"""
from flask import Blueprint, render_template, request

# Create blueprint for order-related routes
orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/')
def index():
    """
    Purchase orders list
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('orders/content.html', page_title='Purchase Orders')
    return render_template('orders/index.html', page_title='Purchase Orders')



@orders_bp.route('/create')
def create():
    """
    Create new purchase order form
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('orders/create_content.html', page_title='New Purchase Order')
    return render_template('orders/create.html', page_title='New Purchase Order')



@orders_bp.route('/<int:order_id>')
def view(order_id):

    
   
    return render_template('orders/view_content.html', 
                         page_title=f'Order #{order_id}',
                         order_id=order_id)
