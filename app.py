from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash, abort, g
from flask_sqlalchemy import SQLAlchemy
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
    from users import Bratuha
    return Bratuha.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
@login_required
def show():
    from queries import save_user_query
    from youtube_search import convert_youtube_results
    from twitter_search import convert_twitter_results

    query_from_form = request.form['title']
    save_user_query(query_from_form)

    youtube_results = convert_youtube_results(query_from_form)
    twitter_results = convert_twitter_results(query_from_form)

    return render_template('results.html', youtuve_videos = youtube_results, tweets = twitter_results)


@app.route('/statistics', methods=['GET'])
@login_required
def statistics():
    from users import user_statistics, verify_user_role, calculate_user_count
    from queries import query_statistics, calculate_query_count

    if verify_user_role() != "admin":

        return 'You have no permission'
    else:

        user_count = calculate_user_count()
        users_statistics = user_statistics()
        queries_statistics = query_statistics()
        query_count = calculate_query_count()

        return render_template('statistics.html', users=users_statistics, users_count=user_count,
                               queries=queries_statistics, queries_count=query_count)


@app.route('/statistics/<id>', methods=['GET'])
def show_queries(id):
    from users import show_user_queries

    queries_of_user = show_user_queries(id)

    return render_template('show_user_queries.html', user_queries=queries_of_user)


@app.route('/query_results', methods=['POST'])
def show_queries_date():
    from queries import show_queries_for_date

    form_query_date_start = request.form['start_date']
    form_query_date_end = request.form['end_date']

    query_list_with_date = show_queries_for_date(form_query_date_start, form_query_date_end)

    return render_template('show_queries_date.html', queries_date = query_list_with_date)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    from users import Bratuha, save_user_to_db
    new_user = Bratuha(request.form['login'], request.form['password'])
    save_user_to_db(new_user)
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    from users import Bratuha
    login = request.form['login']
    password = request.form['password']
    registered_user = Bratuha.query.filter_by(login=login,password=password).first()
    if registered_user is None:
        flash('Login or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

#----------------------------------REST API

@app.route('/supersearch_rest/api/users', methods=['GET'])
def users_list():
    from users import Bratuha
    from queries import Queries

    list_users = []
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
            'count':count
        }

        list_queries = []
        count = 0

        list_users.append(current_user_json)

    return jsonify({'queries': list_users})


#######----------------------------


if __name__ == '__main__':
    app.run()