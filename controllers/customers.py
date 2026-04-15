"""
Customers Controller - Customer management

Handles:
- Listing all customers
- Creating new customers
- Viewing customer details
- Editing customer information
"""
from flask import Blueprint, render_template, request

# Create blueprint for customer routes
customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/')
def index():
    """
    Customers list
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('customers/content.html', page_title='Customers')
    return render_template('customers/index.html', page_title='Customers')


@customers_bp.route('/create')
def create():
    """
    Create new customer
    
    Returns content partial for HTMX, full page for direct navigation
    """
    if request.headers.get('HX-Request'):
        return render_template('customers/create_content.html', page_title='New Customer')
    return render_template('customers/create.html', page_title='New Customer')


@customers_bp.route('/<int:customer_id>')
def view(customer_id):
    """
    View single customer details
    """
    return render_template('customers/view_content.html',
                         page_title=f'Customer #{customer_id}',
                         customer_id=customer_id)
