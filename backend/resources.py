from flask_restful import Resource, Api, reqparse, fields, marshal_with
import sqlalchemy
import pandas as pd
from models import User as user_model, Tracker as tracker_model, Log as log_model, db
from flask import jsonify
from flask import request, send_file
import bcrypt
from datetime import date

# from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from flask_caching import Cache

from celery import Celery

# from flask_celery import make_celery
# from tasks import send, test


cache = Cache()

api = Api()

celery = Celery()


user_fields = {
    "user_id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "email": fields.String,
    "webhook": fields.String,
}

tracker_fields = {
    "tracker_id": fields.Integer,
    "tuser_id": fields.Integer,
    "name": fields.String,
    "desc": fields.String,
    "type": fields.String,
    "settings": fields.String,
    "last_modified": fields.String,
    "last_modified_value": fields.String,
}

log_fields = {
    "log_id": fields.Integer,
    "ltracker_id": fields.Integer,
    "ltype": fields.String,
    "timestamp": fields.String,
    "note": fields.String,
    "value": fields.String,
}


user_req = reqparse.RequestParser()
user_req.add_argument("username", type=str, help="Username is a string", required=True)
user_req.add_argument("password", type=str, help="Password is a string", required=True)
user_req.add_argument("email", type=str, help="Email is a string", required=True)

# update_user_parser = reqparse.RequestParser()
# update_user_parser.add_argument("webhook")

create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument("tracker_id")
create_tracker_parser.add_argument("tuser_id")
create_tracker_parser.add_argument("name")
create_tracker_parser.add_argument("desc")
create_tracker_parser.add_argument("settings")
create_tracker_parser.add_argument("type")


update_tracker_parser = reqparse.RequestParser()
update_tracker_parser.add_argument("name")
update_tracker_parser.add_argument("desc")


create_log_parser = reqparse.RequestParser()
create_log_parser.add_argument("log_id")
create_log_parser.add_argument("ltracker_id")
create_log_parser.add_argument("ltype")
create_log_parser.add_argument("timestamp")
create_log_parser.add_argument("note")
create_log_parser.add_argument("value")


update_log_parser = reqparse.RequestParser()
update_log_parser.add_argument("timestamp")
update_log_parser.add_argument("value")
update_log_parser.add_argument("note")


class Register(Resource):
    def post(self):
        user_data = request.get_json()
        password = user_data["password"].encode()
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = user_model(
            username=user_data["username"],
            email=user_data["email"],
            password=hash_password,
        )
        db.session.add(user)
        db.session.commit()
        return jsonify("login successful")


class Login(Resource):
    def post(self):
        user_data = request.get_json()
        password = user_data["password"].encode()
        print(user_data, password)
        curr_user = user_model.query.filter_by(username=user_data["username"]).first()
        if curr_user is None:
            return jsonify("User doesnt exist")
        elif bcrypt.checkpw(password, curr_user.password):
            access_token = create_access_token(identity=curr_user.user_id)
            print(access_token)
            cache.delete("user_details")
            return jsonify(access_token=access_token)
        else:
            return jsonify("Invalid Password")


# To pass the user_id in memoize - allows multiple users to open in separate browsers at the same time
@cache.memoize(timeout=600)
def hello(curr_user):
    user = user_model.query.get(curr_user)
    return user


class User(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    # @cache.cached(timeout=60, key_prefix="user_details")
    def get(self):
        print("accessed the user endpoint")
        curr_user = get_jwt_identity()
        a = hello(curr_user)
        return a
        # user = user_model.query.get(curr_user)
        # return user


class Tracker(Resource):
    @marshal_with(tracker_fields)
    @jwt_required()
    @cache.memoize(timeout=600)
    def get(self, tracker_id=None):
        curr_user = get_jwt_identity()
        print("accessed the tracker endpoint")
        if tracker_id:
            tracker_data = tracker_model.query.get(tracker_id)
            return tracker_data
        else:
            tracker_data = tracker_model.query.filter_by(tuser_id=curr_user).all()
            return tracker_data

    @marshal_with(tracker_fields)
    @jwt_required()
    def post(self):
        curr_user = get_jwt_identity()
        data = create_tracker_parser.parse_args()
        tracker = tracker_model(
            tuser_id=curr_user,
            name=data.name,
            desc=data.desc,
            settings=data.settings,
            type=data.type,
            last_modified="No Logs Yet!",
            last_modified_value="-",
        )
        db.session.add(tracker)
        db.session.commit()
        return tracker, 200

    @marshal_with(tracker_fields)
    @jwt_required()
    def put(self, tracker_id=None):
        data = update_tracker_parser.parse_args()
        tracker = tracker_model.query.filter_by(tracker_id=tracker_id)
        if tracker:
            tracker.update(data)
            db.session.commit()
            return tracker[0], 200

    @jwt_required()
    def delete(self, tracker_id=None, tuser_id=None):
        tracker = tracker_model.query.get(tracker_id)
        logs = log_model.query.filter_by(ltracker_id=tracker_id)
        for l in logs:
            db.session.delete(l)
            db.session.commit()
        db.session.delete(tracker)
        db.session.commit()
        return "Tracker Deleted", 200


class Log(Resource):
    @marshal_with(log_fields)
    @jwt_required()
    @cache.memoize(timeout=600)
    def get(self, ltracker_id=None, log_id=None):
        if log_id:
            logs = log_model.query.get(log_id)
        else:
            logs = log_model.query.filter_by(ltracker_id=ltracker_id).all()
        return logs
    
    def update_dashboard(self):
        curr_user = get_jwt_identity()
        tracker_data = tracker_model.query.filter_by(tuser_id=curr_user).all()
        for t in tracker_data:
            recent = (
                log_model.query.filter_by(ltracker_id=t.tracker_id)
                .order_by(log_model.timestamp.desc())
                .first()
            )
            td = tracker_model.query.get(t.tracker_id)
            if recent is not None:
                # td.last_modified = f"timestamp={recent.timestamp}, value={recent.value}"
                td.last_modified = recent.timestamp
                td.last_modified_value = recent.value
            else:
                td.last_modified = "No Logs Yet!"
                td.last_modified_value = "-"
            if td.settings is None:
                td.settings = ""
        db.session.commit()

    @marshal_with(log_fields)
    @jwt_required()
    def post(self, ltracker_id=None):
        data = create_log_parser.parse_args()
        log = log_model(
            ltracker_id=ltracker_id,
            timestamp=data.timestamp,
            note=data.note,
            value=data.value,
            ltype=data.ltype,
        )
        db.session.add(log)
        self.update_dashboard()
        return log, 200

    @marshal_with(log_fields)
    @jwt_required()
    def put(self, log_id=None, ltracker_id=None):
        data = update_log_parser.parse_args()
        log = log_model.query.filter_by(log_id=log_id)
        if log:
            log.update(data)
            db.session.commit()
            self.update_dashboard()
            return log[0], 200

    @jwt_required()
    def delete(self, log_id=None, ltracker_id=None):
        log = log_model.query.get(log_id)
        db.session.delete(log)
        db.session.commit()

        print("log deleted")
        self.update_dashboard()

        return "Log Deleted", 200


class Chart(Resource):
    @jwt_required()
    def get(self, tracker_id=None):
        tracker = tracker_model.query.get(tracker_id)
        logs = log_model.query.filter_by(ltracker_id=tracker_id).all()
        if tracker.type == "multiple" or tracker.type == "bool":
            freq = {}
            for log in logs:
                if log.value in freq:
                    freq[log.value] += 1
                else:
                    freq[log.value] = 1
            print(freq)
            graph_data = {"options": [], "count": []}
            graph_data["count"] = list(freq.values())
            if tracker.type == "bool":
                graph_data["options"] = ["yes", "no"]
            else:
                graph_data["options"] = list(freq.keys())
            return graph_data
        elif tracker.type == "td" or tracker.type == "numerical":
            graph_data = {"value": [], "timestamp": []}
            for log in logs:
                graph_data["timestamp"].append(log.timestamp)
                if tracker.type == "td":
                    hr = int(log.value[0:2]) * 60
                    min = int(log.value[3:6])
                    total = hr + min
                    graph_data["value"].append(total)
                else:
                    graph_data["value"].append(log.value)
            return graph_data


class Mail(Resource):
    def get(self):
        users = user_model.query.all()
        emails = []
        entry = {}
        for user in users:
            entry["name"] = user.username
            entry["email"] = user.email
            entry["user_id"] = user.user_id
            emails.append(entry)
            entry = {}
        return emails
        # send.delay(emails)


class Tracker_Report(Resource):
    @marshal_with(tracker_fields)
    def get(self, user_id=None):
        tracker_data = tracker_model.query.filter_by(tuser_id=user_id).all()
        return tracker_data


class Daily_Reminder(Resource):
    @marshal_with(tracker_fields)
    def get(self, user_id=None):
        tracker_data = tracker_model.query.filter_by(tuser_id=user_id).all()
        tracker_list = []
        for tracker in tracker_data:
            today = str(date.today())
            if today not in tracker.last_modified:
                tracker_list.append(tracker)
        return tracker_list


class Download(Resource):
    def post(self, tracker_id=None):
        engine = sqlalchemy.create_engine(
            "sqlite:///project.sqlite3"
        )
        query = "select * from log where ltracker_id={}".format(tracker_id)
        df = pd.read_sql(query, engine)
        name = "./export/{}_logs.csv".format(tracker_id)
        df.to_csv(name)
        # export.delay(tracker_id)
        return send_file(name, as_attachment=True)


api.add_resource(Register, "/api/register")
api.add_resource(Login, "/api/login")
api.add_resource(User, "/api/user")
api.add_resource(Tracker, "/api/trackers", "/api/trackers/<int:tracker_id>")
api.add_resource(
    Log,
    "/api/trackers/<int:ltracker_id>/logs",
    "/api/trackers/<int:ltracker_id>/logs/<int:log_id>",
)
api.add_resource(Chart, "/api/chart/<int:tracker_id>")
api.add_resource(Mail, "/mail")
api.add_resource(Tracker_Report, "/tracker_report/<int:user_id>")
api.add_resource(Daily_Reminder, "/daily_reminder/<int:user_id>")
api.add_resource(Download, "/api/trackers/<int:tracker_id>/download")


# api.add_resource(Webhook, "/api/webhook")
# class Webhook(Resource):
#     @jwt_required()
#     def put(self):
#         curr_user = get_jwt_identity()
#         data = update_user_parser.parse_args()
#         webhhook_user = user_model.query.filter_by(user_id=curr_user)
#         if webhhook_user:
#             webhhook_user.update(data)
#             db.session.commit()
#             return "Webhook added"
