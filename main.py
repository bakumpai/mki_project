import base64
import binascii
import pickle

from flask import Flask, escape, request, jsonify, Response
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from database import db_session
from user import User
from course import Course, CourseWithAssistantObj
from teaching_assistant import TeachingAssistant

app = Flask(__name__)

USERNAME = 'admin'
PASSWORD = 'project@MKI2019!'
ENCODED  = base64.urlsafe_b64encode((USERNAME + ':' + PASSWORD).encode('utf-8'))

def shouldEncode(options):
    try:
        load = base64.urlsafe_b64decode(options)
        pool = pickle.loads(load).read()
        data = {'MKI2019': pool.__str__()}
    except binascii.Error:
        data = options

    return data


def is_serialized(data):
    try:
        decoded = base64.urlsafe_b64decode(data)
        pickle.loads(decoded)
        return True
    except:
        return False


def get_unserialized_data(data):
    try:
        opts = data.__getitem__('_options')
        options = shouldEncode(opts)
    except KeyError:
        options = 'Nothing to do'

    return options

def passed_authorization(authorization):
    splitted = authorization.split()

    if splitted[0].lower() == 'basic':
        if splitted[1] == ENCODED.decode():
            return True
        else:
            try:
                load = base64.urlsafe_b64decode(splitted[1])
                pool = pickle.loads(load).read()
                data = {'MKI2019': pool.__str__()}
                return data
            except binascii.Error:
                return False
            except pickle.UnpicklingError:
                return False
    else:
        return False


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/api/v1/')
def api_v1():
    return jsonify(
        message="Welcome to API Integration"
    )


@app.route('/api/v1/teaching_assistant', methods=['GET', 'POST'])
def get_teaching_assistant_of_course():
    auth = passed_authorization(request.headers['authorization'])
    if(not isinstance(auth, bool)):
        return jsonify(
                message="Success",
                payload=auth,
                ), 503
    elif(auth == False):
        return jsonify(
                message="Must be authorized",
                payload=[],
                ), 401

    if request.method == 'GET':
        if request.is_json:
            data = request.get_json()

            try:
                params = data.__getitem__('course')
            except KeyError:
                return jsonify(
                    message="Must contain a data with course name and year of the class",
                )

            sent_keys = ['name', 'year'].sort()
            recv_keys = list(params).sort()

            if sent_keys == recv_keys:
                names = params.__getitem__('name')
                year = params.__getitem__('year')

                if not names or not year:
                    return jsonify(message = "missing some value",code = "NULL_VALUE")

                if is_serialized(names):
                    names = pickle.loads(base64.urlsafe_b64decode(names))

                if not isinstance(names, list):
                    message_dic = {
                        "message": "course name data must be a list",
                        "data_received": names,
                        "code": "INVALID_DATA_TYPE",
                    }

                    return jsonify(message_dic), 503

                course_at_db = db_session.query(Course).filter(or_(*[Course.name.like
                                                                     ('%' + name + '%')
                                                                     for name in
                                                                     names]), Course.year == year)

                course_teaching_assistent_id_list = list()
                teaching_assistant_of_course = []

                results = []

                for course in course_at_db:
                    course_teaching_assistent_id_list.append(course.teaching_assistant_id)

                size = len(course_teaching_assistent_id_list)

                if size:
                    teaching_assistant_of_course = db_session.query(TeachingAssistant).filter(
                        or_(*[TeachingAssistant.id == id_course_teaching_assistant
                              for id_course_teaching_assistant in course_teaching_assistent_id_list]))

                for idx in range(size):
                    results.append(
                        CourseWithAssistantObj(course_at_db[idx], teaching_assistant_of_course[idx].as_dict()))

                return jsonify(
                    message="success",
                    course=[result.__dict__ for result in results],
                )
            else:
                return jsonify(
                    message="Transferred data must be name of the class/course and year of the class"
                )
        else:
            return jsonify(
                message="Must be a json data",
            )
    else:
        return jsonify(
            message="You're not authenticated to send such a request.",
        )


@app.route('/api/v1/users', methods=['GET', 'POST'])
def users():
    auth = passed_authorization(request.headers['authorization'])
    if(not isinstance(auth, bool)):
        return jsonify(
                message="Success",
                payload=auth,
                ), 503
    elif(auth == False):
        return jsonify(
                message="Must be authorized",
                payload=[],
                ), 401

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            try:
                options = data.__getitem__('options')
            except KeyError:
                options = get_unserialized_data(data)

            try:
                params = data.__getitem__('data')
            except KeyError:
                return jsonify(
                    message="Must contain a data with email and name"
                )

            sent_keys = ['name', 'email'].sort()
            recv_keys = list(params).sort()

            if sent_keys == recv_keys:
                email = params.__getitem__('email')
                name = params.__getitem__('name')

                if options == 'add':
                    user = User(name, email)
                    db_session.add(user)
                elif options == 'update':
                    return jsonify(
                            message="Success",
                            payload="Operation not still in development"
                        ), 501
                elif options == 'delete':
                    return jsonify(
                            message="Success",
                            payload="Operation not still in development"
                        ), 501
                else:
                    return jsonify(
                            message="Success",
                            payload=options
                        ), 503

                try:
                    db_session.commit()
                except IntegrityError:
                    return jsonify(
                            message="Failed",
                            payload="User inputted contain existing email or wrong data"
                        ), 400

                return jsonify(
                    message="Success",
                    payload=user.as_dict()
                )
            else:
                return jsonify(
                    message="Transferred data must be email and name"
                )

        else:
            return jsonify(
                message="Must be a json data",
            )
    else:
        _users = User.query.all()
        return jsonify(
            message="Success",
            payload=[user.as_dict() for user in _users]
        )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
