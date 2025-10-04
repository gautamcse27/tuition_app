from flask import Blueprint

# Specify template_folder to point to the 'templates' directory within 'admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

from . import routes  # Import routes to register with the blueprint
