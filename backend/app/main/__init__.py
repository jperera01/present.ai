from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.get('/')
def index():
    return render_template("index.html")


@main_bp.get('/login')
def login():
    return render_template("login.html")


@main_bp.get('/signup')
def signup():
    return render_template("signup.html")


@main_bp.get('/present')
def present():
    return render_template("present.html")
