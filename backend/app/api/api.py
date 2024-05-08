import uuid
from flask_restx import Resource, Namespace
from app.exts import p_sessions
from flask import request, render_template, redirect, make_response
import pymongo
from app.models import User
from flask_jwt_extended import decode_token
import datetime

api_ns = Namespace('api', description='namespace for general apis')

def minutes_to_readable(length):
    try:
        time_float = float(length)
    except (ValueError, TypeError):
        return {"minutes": 0, "seconds": 0}

    minutes = int(time_float)
    seconds = (time_float - minutes) * 60
    return {"minutes": minutes, "seconds": int(seconds)}


@api_ns.route('/dashboard/home/total_presentations')
class TotalPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        query = p_sessions.find({"user_id": db_user.id})

        resp = make_response(f"{len(list(query))}")

        resp.headers['content-type'] = 'text/html'

        return resp


@api_ns.route('/dashboard/home/average_presentations')
class AveragePresentationLength(Resource):
    def get(self):
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()
        if not db_user:
            return "User not found", 404

        query = p_sessions.find({"user_id": db_user.id})

        total_length = 0
        count = 0
        for session in query:
            if 'length' in session:
                total_length += session['length']
                count += 1
        
        if count == 0:
            average_length = 0
        else:
            average_length = total_length / count

        resp = make_response(f"{int(average_length)}")

        resp.headers['content-type'] = 'text/html'

        return resp


@api_ns.route('/dashboard/home/recent_presentations')
class RecentPresentations(Resource):
    def get(self):
        token = request.cookies.get('token')

        token_decoded = decode_token(token)

        email = token_decoded['sub']

        db_user = User.query.filter_by(email=email).first()

        query = p_sessions.find({"user_id": db_user.id}).sort(
            'timestamp', pymongo.DESCENDING).limit(3)

        result = [
            {**obj, 'length': minutes_to_readable(obj['length']), 'timestamp': obj['timestamp'].strftime('%m/%d/%Y'), 'number': i + 1}
            for i, obj in enumerate(list(query))
        ]

        resp = make_response(render_template(
            "dashboard/partials/recent.j2", recent=result))

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
            "name": request.form['present_name'],
            "description": request.form['present_description'],
            "length": float(request.form['present_length']),
            "confidences": [],
            "wpm": [],
            "timestamp": datetime.datetime.now()
        })

        resp = make_response(render_template("present.j2"))

        resp.headers['HX-Redirect'] = '/present'

        resp.set_cookie('present_id', presentation_id)

        return resp


@api_ns.route('/init-present')
class InitPresetn(Resource):
    def post(self):
        presentation_id = request.cookies.get('present_id')

        presentation = p_sessions.find_one({ "presentation_id": presentation_id })
        print(presentation['length'])

        return {
            'length': presentation['length']
        }

@api_ns.route('/summary/<string:present_id>')
class Summary(Resource):
    def get(self, present_id):
        try:
            length = float(request.args.get('t'))

            document = p_sessions.find_one({"presentation_id": present_id})
            new_length = document["length"] - length

            p_sessions.update_one({ "presentation_id": present_id },
                                {"$set": {"length": new_length }})
        except Exception:
            ...

        presentation = p_sessions.find_one({ "presentation_id": present_id })
        lst = presentation['confidences']
        wpms = presentation['wpm']

        data = {
            "name": presentation['name'],
            "description": presentation['description'],
            "length": minutes_to_readable(float(presentation['length'])),
            "avg_confidence": int(sum(lst) / len(lst) if lst else 0),
            "confidence_values": lst,
            "confidence_intervals": [f"{5 * (i+1)} seconds" for i in range(len(lst))],
            'wpm': wpms,
            'avg_wpm': int(sum(wpms) / len(wpms) if wpms else 0),
            "wpm_intervals": [f"{5 * (i+1)} seconds" for i in range(len(wpms))],
        }
        print("presentation", presentation)
        print("data", data)

        resp = make_response(render_template("dashboard/summary.j2", presentation=data))
        resp.headers['content-type'] = 'text/html'

        return resp


