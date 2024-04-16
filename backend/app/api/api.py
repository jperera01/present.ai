from flask_restx import Resource, Namespace
from app.exts import p_sessions
from flask import request, render_template, redirect, make_response
import pymongo

api_ns = Namespace('api', description='namespace for general apis')


@api_ns.route('/dashboard/home/total_presentations')
class TotalPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        query = p_sessions.find({"id": token})

        resp = make_response(f"{len(list(query))}")

        resp.headers['content-type'] = 'text/html'

        return resp


@api_ns.route('/dashboard/home/recent_presentations')
class RecentPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        query = p_sessions.find({"id": token}).sort(
            'field', pymongo.ASCENDING).limit(3)

        print(query)

        resp = make_response(render_template(
            "dashboard/partials/recent.j2", recent=list(query)))

        resp.headers['content-type'] = 'text/html'

        return resp
