from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes, git_manager, grpc_manager
