from app import db



class Bratuha(db.Model):
    __tablename__ = 'bratuhas'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        #return unicode(self.id)
        return int(self.id)

    def __repr__(self):
        return "<User(login='%s', password='%s')>" % (self.login, self.password)
