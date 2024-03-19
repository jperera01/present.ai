from flask import Blueprint, render_template
from app.models import User
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard',
                         __name__,
                         url_prefix="/dashboard")


@dashboard_bp.get('/@me')
def me():
    return render_template("dashboard.j2")
