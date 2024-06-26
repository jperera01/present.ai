from flask import Blueprint, render_template, request, redirect, session
from flask_jwt_extended import decode_token
from app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.get('/test')
def test():
    return render_template("test.j2")


@main_bp.get('/')
def index():
    return render_template("index.j2")


@main_bp.get('/login')
def login():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        if db_user is None:
            return render_template("login.j2")

        return redirect('/dashboard/home')
    except Exception:
        return render_template("login.j2")


@main_bp.get('/signup')
def signup():
    try:
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        if db_user is None:
            return render_template("signup.j2")

        return redirect('/dashboard/home')
    except Exception:
        return render_template("signup.j2")


@main_bp.get('/present')
def present():
    """
    if str(request.referrer).split('/')[-1] != 'present':
        resp = redirect('/dashboard/home')

        return resp

    session['location'] = 'present'
    """

    return render_template("present.j2")


@main_bp.get('/pricing')
def pricing():
    return render_template("pricing.j2")


"""
@main_bp.get('/')
def present():
    if str(request.referrer).split('/')[-1] != 'present':
        resp = redirect('/dashboard/home')

        return resp

    session['location'] = 'present'

    return render_template("present.j2")
"""
