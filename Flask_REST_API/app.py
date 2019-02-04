from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)
app.config.update({
    'DEBUG': True,
    'SECRET_KEY': 'super_secret_key',
    'PROPAGATE_EXCEPTIONS': True
})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./user.db'
db = SQLAlchemy(app)

from src.db.user_model import User
from src.db.counter_model import Counter
from src.error.user_error_handler import UserErrorHandler
from src.error.error_handler import ErrorHandler

api = Api(app)
db.drop_all()
db.create_all()
User.db_init()
Counter.db_init()


@app.errorhandler(Exception)
def unhandled_exception(e):
    commonErrorMessage = ErrorHandler.checkIsCorrectUser(e)
    return jsonify({"Message": commonErrorMessage, "success": False})


@app.route('/users', methods=['Get'])
def getAll():
    return User.getUsers()


@app.route('/users/age', methods=['Get'])
def getUsersByName():
    return User.getUsersByAge()


@app.route('/users/name', methods=['Get'])
def getUsersByAge():
    return User.getUsersByName()


@app.route('/users/counter', methods=['Get'])
def getUsersCounter():
    return User.getUsersCounter()


@app.route('/users/post', methods=['POST'])
def createUser():
   errorMessage = UserErrorHandler.checkIsCorrectUser(request.json)
   if (errorMessage is ''):
       return User.addUser(request.json)
   else:
       return jsonify({"Message": errorMessage, "success": False})


@app.route('/users/delete', methods=['DELETE'])
def delete():
    errorMessage = UserErrorHandler.checkIsUserAgeCorrect(request.json)
    if (errorMessage is ''):
        return User.delUsers(request.json)
    else:
        return jsonify({"Message": errorMessage, "success": False})


if __name__ == '__main__':
    app.run()
