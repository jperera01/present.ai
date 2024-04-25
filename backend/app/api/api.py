import uuid
from flask_restx import Resource, Namespace
from app.exts import p_sessions
from flask import request, render_template, redirect, make_response
import pymongo
from app.models import User
from flask_jwt_extended import decode_token

api_ns = Namespace('api', description='namespace for general apis')


@api_ns.route('/dashboard/home/total_presentations')
class TotalPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        query = p_sessions.find({"user_id": token})

        resp = make_response(f"{len(list(query))}")

        resp.headers['content-type'] = 'text/html'

        return resp


@api_ns.route('/dashboard/home/recent_presentations')
class RecentPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        query = p_sessions.find({"user_id": token}).sort(
            'field', pymongo.ASCENDING).limit(3)

        print(query)

        resp = make_response(render_template(
            "dashboard/partials/recent.j2", recent=list(query)))

        resp.headers['content-type'] = 'text/html'

        return resp


@api_ns.route('/dashboard/home/create_presentations')
class CreatePresentation(Resource):
    def post(self):
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        presentation_id = str(uuid.uuid4())

        p_sessions.insert_one({
            "user_id": db_user.id,
            "presentation_id": presentation_id,
            "name": request.form['present_name']
        })

        resp = make_response(render_template("present.j2"))

        resp.headers['HX-Redirect'] = '/present'

        resp.set_cookie('present_id', presentation_id)

        return resp
