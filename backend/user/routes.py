from flask import Flask
from ..app import app
from flask_restful import Resource, reqparse, Api
from ..user.models import User

@app.route('user/signup', methods=['GET'])
def signup():
    user = User()
    return user.signup()
