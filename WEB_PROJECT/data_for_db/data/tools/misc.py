from flask import make_response, jsonify

from data_for_db.data.users import User


def make_resp(message, status):
    resp = make_response((message, status))
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp

# def create_jwt_response(user):
#     cp_user = User(name=user.name, email=user.email)
#     # cp_user = {'name':user.   name, 'email':user.email)
#     token = {'token': create_jwt(identity=cp_user)}
#     return make_resp(jsonify(token), 200)
