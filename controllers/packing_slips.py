"""
Packing Slips Controller
"""
from flask import Blueprint, render_template, request

packing_slips_bp = Blueprint('packing_slips', __name__)


@packing_slips_bp.route('/')
def index():
    """List all packing slips"""
    if request.headers.get('HX-Request'):
        return render_template('packing_slips/content.html', page_title='Packing Slips')
    return render_template('packing_slips/index.html', page_title='Packing Slips')


@packing_slips_bp.route('/create')
def create():
    """Create new packing slip form"""
    if request.headers.get('HX-Request'):
        return render_template('packing_slips/create_content.html', page_title='New Packing Slip')
    return render_template('packing_slips/create.html', page_title='New Packing Slip')


@packing_slips_bp.route('/<int:slip_id>')
def view(slip_id):
    """View single packing slip"""
    return render_template('packing_slips/view_content.html',
                         page_title=f'Packing Slip #{slip_id}',
                         slip_id=slip_id)
