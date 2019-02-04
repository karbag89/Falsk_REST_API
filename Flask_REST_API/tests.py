import unittest
import json
from app import app, db
from src.db.user_model import User, Counter


class UsersTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        db.drop_all()
        db.create_all()
        with open('initUsers.json') as f:
            self.data = json.load(f)
        users = self.data['users']
        for user in users:
            new_user = User(user)
            db.session.add(new_user)
        init_counter = Counter(0)
        db.session.add(init_counter)
        db.session.commit()
        db.session.commit()

    def test_getUsers(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json)
        usersDataFromFile = self.data['users']
        usersDataFromDB = User.query.all()
        for cycle in range(len(usersDataFromDB)):
            self.assertEqual(usersDataFromDB[cycle].name, usersDataFromFile[cycle]['name'])
            self.assertEqual(usersDataFromDB[cycle].age, usersDataFromFile[cycle]['age'])
            self.assertEqual(usersDataFromDB[cycle].occupation, usersDataFromFile[cycle]['occupation'])

    def test_getUsersCounter(self):
        response = self.client.get("/users/counter")
        self.assertEqual(response.status_code, 200)
        value = str(response.json)[len(str(response.json))-16:-1]
        self.assertEqual(value, "'success': True")
        count = Counter.query.first().count
        self.assertEqual(count, 0)

    def test_getUsersByAge(self):
        response = self.client.get("/users/age")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json)
        usersDataFromDB = User.query.order_by(User.age.asc()).all()
        for item in range(len(usersDataFromDB)-1):
            assert ((int(usersDataFromDB[item].age)) < (int(usersDataFromDB[item+1].age)))

    def test_getUsersByName(self):
        response = self.client.get("/users/name")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json)
        usersDataFromDB = User.query.order_by(User.name.asc()).all()
        for item in range(len(usersDataFromDB) - 1):
            assert ((ord(usersDataFromDB[item].name[:1])) < (ord(usersDataFromDB[item + 1].name[:1])))

    def test_addUser(self):
        response = self.client.get('/users/create')
        self.assertEqual(response.status_code, 200)
        self.data = {"name": "Post", "age": 102, "occupation": "Network Engineer"}
        with app.app_context():
            User.addUser(self.data)
        with open('initUsers.json') as f:
            data = json.load(f)
        usersDataFromFile = data['users']
        usersDataFromDB = User.query.all()
        for item in range(len(usersDataFromDB)):
            if item == len(usersDataFromDB)-1:
                self.assertEqual(usersDataFromDB[item].name, self.data["name"])
                self.assertEqual(usersDataFromDB[item].age, self.data["age"])
                self.assertEqual(usersDataFromDB[item].occupation, self.data["occupation"])
            else:
                self.assertEqual(usersDataFromDB[item].name, usersDataFromFile[item]['name'])
                self.assertEqual(usersDataFromDB[item].age, usersDataFromFile[item]['age'])
                self.assertEqual(usersDataFromDB[item].occupation, usersDataFromFile[item]['occupation'])

    def test_delUsers(self):
        response = self.client.get("/users/delete")
        self.assertEqual(response.status_code, 200)
        self.data = {"age": 33}
        with app.app_context():
            User.delUsers(self.data)
        usersDataFromDB = User.query.order_by(User.age.desc()).all()
        assert ((int(usersDataFromDB[0].age)) < self.data["age"])

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
