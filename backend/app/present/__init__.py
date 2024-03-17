from flask import Blueprint, render_template

present_bp = Blueprint('present', __name__)


@present_bp.get('/present')
def index():
    return render_template("present.html")
