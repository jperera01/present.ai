from flask_restx import Resource, Namespace, fields
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import request, render_template, redirect, make_response
from datetime import timedelta

auth_ns = Namespace('auth', description='namespace for authentication apis')

signup_model = auth_ns.model(
    "SignUp",
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(),
        'password': fields.String()
    }
)


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        email = request.form['email']

        db_user = User.query.filter_by(email=email).first()

        if db_user is not None:
            message = "user already exists"

            resp = make_response(render_template("error.j2", message=message))

            resp.status = 400

            resp.content_type = 'text/html'

            return resp

        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=email,
            password=generate_password_hash(request.form['password'])
        )

        new_user.save()

        token = create_access_token(identity=new_user.email,
                                    expires_delta=timedelta(days=3))

        resp = make_response({}, 200)

        resp.headers['HX-Redirect'] = '/dashboard/home'

        resp.set_cookie('token', token)

        return resp


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        email = request.form['email']
        password = request.form['password']

        db_user = User.query.filter_by(email=email).first()
        error_message = 'authentication error.'

        if db_user is None:
            resp = make_response(render_template("error.j2",
                                                 message=error_message), 200)

            resp.content_type = 'text/html'

            return resp

        if check_password_hash(db_user.password,  password):
            token = create_access_token(identity=db_user.email,
                                        expires_delta=timedelta(days=3))

            resp = make_response({}, 200)
            resp.headers['HX-Redirect'] = '/dashboard/home'

            resp.set_cookie('token', token)

            return resp

        resp = make_response(render_template(
            "error.j2", message=error_message))

        resp.status = 400

        resp.content_type = 'text/html'

        return resp


@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        resp = make_response({}, 200)
        resp.headers['HX-Redirect'] = '/'

        resp.delete_cookie('token')

        return resp
