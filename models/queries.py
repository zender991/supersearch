from app import db
from flask_login import current_user

class Queries(db.Model):

    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, search_query, user_id):
        self.search_query = search_query
        self.user_id = user_id


def save_user_query(query_from_form):

    user_id = current_user.get_id()
    user_query = Queries(search_query=query_from_form, user_id=user_id)
    db.session.add(user_query)
    db.session.commit()


def query_statistics():

    query_list = []
    for instance in db.session.query(Queries):
        query_list.append(instance.search_query)

    unique_quries = []
    for instance in query_list:
        if instance not in unique_quries:
            unique_quries.append(instance)

    query_with_count = []
    for instance in unique_quries:
        query_with_count_json = {
            "query": instance,
            "count": query_list.count(instance)
        }
        query_with_count.append(query_with_count_json)

    return query_with_count


def calculate_query_count():

    query_count = db.session.query(Queries).count()

    return query_count


def show_queries_for_date(form_query_date_start, form_query_date_end):

    query_list_with_date = []
    for instance in db.session.query(Queries).filter(Queries.date >= form_query_date_start).filter(
                    Queries.date <= form_query_date_end):

        query_json = {
            "query": instance.search_query,
            "date": instance.date
        }
        query_list_with_date.append(query_json)

    return query_list_with_date