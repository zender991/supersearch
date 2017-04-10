from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash, abort, g
import json
from flask_sqlalchemy import SQLAlchemy
from youtube_search import youtube_search
from twitter_search import twitter_search
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testbd.sqlite'
app.config['SECRET_KEY'] = 'zxczxasdsad'
#app.config.from_object(os.environ['APP_SETTINGS'])


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    from test_base import Bratuha
    return Bratuha.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')



@app.route('/results', methods=['POST'])
@login_required
def show():
    from test_base import Queries
    from test_base import Bratuha

    form_query = request.form['title']

    user1 = current_user.get_id()

    query1 = Queries(search_query=form_query, bratuha_id = user1)
    db.session.add(query1)
    db.session.commit()

    youtube_videos = youtube_search(form_query)

    youtube_videos_json = json.dumps(youtube_videos)

    youtube_videos_list = json.loads(youtube_videos_json)

    list_tweets = twitter_search(form_query)

    twitter_json = json.dumps(list_tweets)

    twitter_list_template = json.loads(twitter_json)

    return render_template('results.html', yt_vid = youtube_videos_list, tweets = twitter_list_template)


@app.route('/statistics', methods=['GET'])
@login_required
def statistics():
    from test_base import Bratuha
    from test_base import Queries

    user = current_user.get_id()

    for instance in db.session.query(Bratuha).filter(Bratuha.id == user):
        cur_user = instance.name

    if cur_user != "admin":

        return 'You have no permission'
    else:

        user_count = db.session.query(Bratuha).count()

        list_users = []
        list_queries = []
        count = 0

        for instance in db.session.query(Bratuha):
            for br in db.session.query(Queries).filter(instance.id == Queries.bratuha_id):
                list_queries.append(br.search_query)
                count = count + 1

            temp_json = {
                'id': instance.id,
                'login': instance.login,
                'password': instance.password,
                'queryes': list_queries,
                'count': count
            }

            list_queries = []
            count = 0

            list_users.append(temp_json)

    ########----------QUERIES---------------

        qu_list = []

        for instance in db.session.query(Queries):
            qu_list.append(instance.search_query)

        print(qu_list)

        q_list = []
        for instance in qu_list:
            if instance not in q_list:
                q_list.append(instance)

        b = []
        for i in q_list:
            count_json = {
                "query": i,
                "count": qu_list.count(i)
            }

            b.append(count_json)

        query_count = db.session.query(Queries).count()

        return render_template('statistics.html', users=list_users, count=user_count, queries=b, q_count=query_count)


@app.route('/statistics/<id>', methods=['GET'])
def show_queries(id):
    from test_base import Bratuha
    from test_base import Queries
    query_list = []
    for instance, br in db.session.query(Queries, Bratuha).filter(Queries.bratuha_id == id).filter(Queries.bratuha_id == Bratuha.id):
        query_list.append(instance.search_query)

    return render_template('show_user_queries.html',queries=query_list)


@app.route('/query_results', methods=['POST'])
def show_queries_date():
    from test_base import Queries
    from test_base import Bratuha
    query_list_date = []

    form_query_date_start = request.form['start_date']
    form_query_date_end = request.form['end_date']

    for instance in db.session.query(Queries).filter(Queries.date > form_query_date_start).filter(Queries.date < form_query_date_end):
        query_json = {
            "query": instance.search_query,
            "date": instance.date
        }

        query_list_date.append(query_json)


    return render_template('show_queries_date.html', queries_date = query_list_date)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    from test_base import Bratuha
    user = Bratuha(request.form['login'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    from test_base import Bratuha
    login = request.form['login']
    password = request.form['password']
    registered_user = Bratuha.query.filter_by(login=login,password=password).first()
    if registered_user is None:
        flash('Login or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    #return redirect(request.args.get('next') or url_for('index'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

#----------------------------------








if __name__ == '__main__':
    app.run()