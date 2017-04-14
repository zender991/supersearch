from app import db
from sqlalchemy.orm import relationship
from flask_login import current_user
from queries import Queries  #need for relationship


class Bratuha(db.Model):
    __tablename__ = 'bratuhas'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))
    name = db.Column(db.String(80))
    search_queries = relationship("Queries", backref="bratuha", lazy='dynamic')

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


def verify_user_role():
    user_id = current_user.get_id()
    for instance in db.session.query(Bratuha).filter(Bratuha.id == user_id):
        logged_in_user = instance.name

    return logged_in_user


def user_statistics():
    from queries import Queries

    user_statistics = []
    list_queries = []
    count = 0

    for instance in db.session.query(Bratuha):
        for query in db.session.query(Queries).filter(instance.id == Queries.bratuha_id):
            list_queries.append(query.search_query)
            count = count + 1

        current_user_json = {
            'id': instance.id,
            'login': instance.login,
            'queryes': list_queries,
            'count': count
        }

        list_queries = []
        count = 0

        user_statistics.append(current_user_json)

    return user_statistics


def calculate_user_count():

    user_count = db.session.query(Bratuha).count()

    return user_count


def show_user_queries(id):

    queries_of_user = []
    for user, query in db.session.query(Queries, Bratuha).filter(Queries.bratuha_id == id).filter(Queries.bratuha_id == Bratuha.id):
        queries_of_user.append(user.search_query)

    return queries_of_user


def save_user_to_db(new_user):
    db.session.add(new_user)
    db.session.commit()








