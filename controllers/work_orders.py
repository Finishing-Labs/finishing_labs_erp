"""
Work Orders Controller
"""
from flask import Blueprint, render_template, request

work_orders_bp = Blueprint('work_orders', __name__)


@work_orders_bp.route('/')
def index():
    """List all work orders"""
    if request.headers.get('HX-Request'):
        return render_template('work_orders/content.html', page_title='Work Orders')
    return render_template('work_orders/index.html', page_title='Work Orders')



@work_orders_bp.route('/builder')
def builder():
    """Work order builder interface"""
    if request.headers.get('HX-Request'):
        return render_template('work_orders/builder_content.html', page_title='Work Order Builder')
    return render_template('work_orders/builder.html', page_title='Work Order Builder')



@work_orders_bp.route('/<int:wo_id>')
def view(wo_id):
    """View single work order"""

    
   
    return render_template('work_orders/view_content.html',
                             page_title=f'Work Order {wo_id}',
                             wo_id=wo_id)

