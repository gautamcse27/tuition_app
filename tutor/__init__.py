from flask import Blueprint

tutor_bp = Blueprint('tutor', __name__, url_prefix='/tutor')

from . import routes  # Import routes to register
