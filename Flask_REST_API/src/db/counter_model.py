from app import db


class Counter(db.Model):
    __tablename__ = 'counter'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)

    def __init__(self, count):
        self.count = count

    @staticmethod
    def db_init():
        init_counter = Counter(0)
        db.session.add(init_counter)
        db.session.commit()
