from flask import abort, request
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from main import successful_response, users_collection
from models import User

class Signup(Resource):
    def post(self):
        json_data = request.get_json()

        user = User(json_data)
        error = user.validate()
        if error:
            return abort(400, description=error)

        db_user = users_collection.find_one(
            {"username": user.username},
            {"username": 1})
        if db_user:
            return abort(400, description="Username already taken.")

        new_user = {
            "username": user.username,
            "password": generate_password_hash(user.password),
            "account_type": user.account_type.name
        }

        res = users_collection.insert_one(new_user)
        new_user["_id"] = str(res.inserted_id)

        login_user(User(new_user))

        new_user.pop("password")
        return new_user, 200