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

    return render_template('orders/content.html', page_title='Purchase Orders')



@orders_bp.route('/create')
def create():

    return render_template('orders/create_content.html', page_title='New Purchase Order')



@orders_bp.route('/<int:order_id>')
def view(order_id):

    
   
    return render_template('orders/view_content.html', 
                         page_title=f'Order #{order_id}',
                         order_id=order_id)
