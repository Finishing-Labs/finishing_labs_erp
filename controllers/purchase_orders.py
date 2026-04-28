"""
Purchase Orders Controller
"""
from flask import Blueprint, render_template, request

purchase_orders_bp = Blueprint('purchase_orders', __name__)


@purchase_orders_bp.route('/')
def index():
    """List all purchase orders"""
    if request.headers.get('HX-Request'):
        return render_template('purchase_orders/content.html', page_title='Purchase Orders')
    return render_template('purchase_orders/index.html', page_title='Purchase Orders')



@purchase_orders_bp.route('/create')
def create():
    """Create new purchase order form"""
    if request.headers.get('HX-Request'):
        return render_template('purchase_orders/create_content.html', page_title='New Purchase Order')
    return render_template('purchase_orders/create.html', page_title='New Purchase Order')



@purchase_orders_bp.route('/<int:order_id>')
def view(order_id):

    
   
    return render_template('purchase_orders/view_content.html', 
                         page_title=f'Order #{order_id}',
                         order_id=order_id)
