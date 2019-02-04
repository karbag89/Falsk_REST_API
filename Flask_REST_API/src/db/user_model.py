from flask import jsonify
from app import db
import json
from src.db.counter_model import Counter


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(50))

    def __init__(self, user):
        self.name = user['name']
        self.age = user['age']
        self.occupation = user['occupation']

    @staticmethod
    def db_init():
        with open('initUsers.json') as f:
            data = json.load(f)
        users = data['users']
        for user in users:
            new_user = User(user)
            db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def getUsers():
        users = User.query.all()
        user_list = []
        for user in users:
            user_info = "{" + "\"name\"" + ":" + '"' + str(user.name) + '"' + "," + "\"age\"" + ":" + '"' + str(
                user.age) + '"' + "," + "\"occupation\"" + ":" + '"' + str(user.occupation) + '"' + "}"
            user_list.append(user_info)
        user_json = "'" + '{"success": true, "users" : ' + str(user_list) + "}" + "'"
        return user_json

    @staticmethod
    def getUsersByName():
        count = Counter.query.first().count
        counter = Counter.query.get(1)
        counter.count = count + 1
        db.session.commit()
        users = User.query.order_by(User.name.asc()).all()
        user_list = []
        for user in users:
            user_info = "{" + "\"name\"" + ":" + '"' + str(user.name) + '"' + "," + "\"age\"" + ":" + '"' + str(
                user.age) + '"' + "," + "\"occupation\"" + ":" + '"' + str(user.occupation) + '"' + "}"
            user_list.append(user_info)
        user_json = "'" + '{"success": true, "users" : ' + str(user_list) + '}' + "'"
        return user_json

    @staticmethod
    def getUsersCounter():
        count = Counter.query.first().count
        return jsonify({"success": True, "Counter": count})

    @staticmethod
    def getUsersByAge():
        users = User.query.order_by(User.age.asc()).all()
        user_list = []
        for user in users:
            user_info = "{" + "\"name\"" + ":" + '"' + str(user.name) + '"' + "," + "\"age\"" + ":" + '"' + str(
                user.age) + '"' + "," + "\"occupation\"" + ":" + '"' + str(user.occupation) + '"' + "}"
            user_list.append(user_info)
        user_json = "'" + '{"success": true, "users" : ' + str(user_list) + '}' + "'"
        return user_json

    @staticmethod
    def addUser(user):
        new_user = User(user)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True})

    @staticmethod
    def delUsers(user):
        age = user['age']
        users = User.query.filter(age < User.age).all()
        for user in users:
            db.session.delete(user)
            db.session.commit()
        return jsonify({"success": True})
