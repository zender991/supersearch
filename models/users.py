from flask import redirect, url_for, flash,request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user, login_user
from sqlalchemy.orm import relationship

from app import db
from models.queries import Queries  #need for relationship


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))
    user_role = db.Column(db.String(80), server_default='user')
    search_queries = relationship("Queries", backref="user", lazy='dynamic')

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
    for instance in db.session.query(User).filter(User.id == user_id):
        logged_in_user = instance.user_role

    return logged_in_user


def user_statistics():
    from models.queries import Queries

    user_statistics = []
    list_queries = []
    count = 0

    for instance in db.session.query(User):
        for query in db.session.query(Queries).filter(instance.id == Queries.user_id):
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

    user_count = db.session.query(User).count()

    return user_count


def show_user_queries(id):

    queries_of_user = []
    for user, query in db.session.query(Queries, User).filter(Queries.user_id == id).filter(Queries.user_id == User.id):
        queries_of_user.append(user.search_query)

    return queries_of_user


def save_user_to_db(new_user):

    db.session.add(new_user)
    db.session.commit()


def verify_user(login, password):

    search_user_in_db = db.session.query(User.password).filter(User.login == login).first()
    check_password = check_password_hash(search_user_in_db.password, password)

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    if check_password is True:
        registered_user = User.query.filter_by(login=login).first()
    else:
        flash('Login or Password is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')


def crypt_password(login_from_form, password_from_form):

    pw_hash = generate_password_hash(password_from_form).decode('utf-8')
    new_user = User(login_from_form, pw_hash)

    return new_user

def reset_pass(password_from_form_first, password_from_form_second):
    if password_from_form_first == password_from_form_second:
        user_id = current_user.get_id()
        pw_hash = generate_password_hash(password_from_form_first).decode('utf-8')

        current_user_from_db = db.session.query(User).filter(User.id == user_id).first()
        current_user_from_db.password = pw_hash
        db.session.add(current_user_from_db)
        db.session.commit()

    else:
        return "Passwords in the fields are different"


def show_queries_in_my_account():
    queries_of_user = []
    current_user_id = current_user.get_id()
    for user, query in db.session.query(Queries, User).filter(Queries.user_id == current_user_id).filter(
                    Queries.user_id == User.id):
        queries_of_user.append(user.search_query)

    return queries_of_user
