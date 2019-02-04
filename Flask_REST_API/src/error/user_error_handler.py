class UserErrorHandler:
    @staticmethod
    def checkIsCorrectUser(json):
        age = json['age']
        name = json['name']
        occupation = json['occupation']
        if name is '' or str(name).isdigit() or str(name).isspace() or len(str(name)) >= 30:
            return "Name is incorrect"
        elif int(age) > 150 or int(age) <= 0:
            return "Age is incorrect"
        elif occupation is '' or str(occupation).isdigit() or str(occupation).isspace() or len(str(occupation)) >= 50:
            return "Occupation is incorrect"
        else:
            return ''

    @staticmethod
    def checkIsUserAgeCorrect(json):
        age = json['age']
        if int(age) > 150 or int(age) <= 0:
            return "Age is incorrect"
        else:
            return ''
