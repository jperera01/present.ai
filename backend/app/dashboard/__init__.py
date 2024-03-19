from flask import Blueprint, render_template, redirect, request
from app.models import User
from flask_jwt_extended import decode_token

dashboard_bp = Blueprint('dashboard',
                         __name__,
                         url_prefix="/dashboard")


@dashboard_bp.get('/@me')
def me():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        if db_user is None:

            return redirect("/login")

        name = f"{db_user.first_name} {db_user.last_name}"

        return render_template('dashboard.j2', name=name)
    except Exception:
        return redirect("/login")
