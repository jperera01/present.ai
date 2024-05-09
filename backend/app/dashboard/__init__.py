from flask import Blueprint, render_template, redirect, request
from app.models import User
from flask_jwt_extended import decode_token
from app.exts import p_sessions
from app.api.api import minutes_to_readable

dashboard_bp = Blueprint('dashboard',
                         __name__,
                         url_prefix="/dashboard")


@dashboard_bp.get('/home')
def home():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        if db_user is None:
            return redirect("/login")

        name = f"{db_user.first_name} {db_user.last_name}"

        return render_template('dashboard/home.j2', name=name)
    except Exception:
        return redirect("/login")


@dashboard_bp.get('/present')
def present():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        if db_user is None:
            return redirect("/login")

        name = f"{db_user.first_name} {db_user.last_name}"
        return render_template('dashboard/present.j2', name=name)
    except Exception:
        return redirect("/login")


@dashboard_bp.get('/presentations')
def presentations():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        query = list(p_sessions.find({"user_id": db_user.id}))

        length = len(query)

        result = [
            {**obj, 'length': minutes_to_readable(obj['length']), 'timestamp': obj['timestamp'].strftime('%m/%d/%Y'), 'number': length - i}
            for i, obj in enumerate(list(query))
        ]

        if db_user is None:
            return redirect("/login")

        name = f"{db_user.first_name} {db_user.last_name}"
        return render_template('dashboard/presentations.j2', name=name, presentations=result)
    except Exception:
        return redirect("/login")
