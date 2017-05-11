from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, g
from flask_login import LoginManager, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

app.config.from_object('config')
heroku = Heroku(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    from models.users import User
    return User.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
@login_required
def show():
    from models.queries import save_user_query
    from youtube_search import convert_youtube_results
    from twitter_search import convert_twitter_results

    with open("words.txt") as file:
        array = [row.strip() for row in file]

    query_from_form = request.form['title']
    save_user_query(query_from_form)

    if query_from_form not in array:

        youtube_results = convert_youtube_results(query_from_form)
        twitter_results = convert_twitter_results(query_from_form)

        return render_template('results.html', youtuve_videos = youtube_results, tweets = twitter_results)
    else:
        flash('Bad word. Shame on you')
        return render_template('index.html')


@app.route('/statistics', methods=['GET'])
@login_required
def statistics():
    from models.users import user_statistics, verify_user_role, calculate_user_count
    from models.queries import query_statistics, calculate_query_count

    if verify_user_role() != "user":
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
    from models.users import show_user_queries

    queries_of_user = show_user_queries(id)

    return render_template('show_user_queries.html', user_queries=queries_of_user)


@app.route('/query_results', methods=['POST'])
def show_queries_date():
    from models.queries import show_queries_for_date

    form_query_date_start = request.form['start_date']
    form_query_date_end = request.form['end_date']

    query_list_with_date = show_queries_for_date(form_query_date_start, form_query_date_end)

    return render_template('show_queries_date.html', queries_date = query_list_with_date)


@app.route('/my_account', methods=['GET'])
@login_required
def my_account():
    from models.users import show_queries_in_my_account
    from models.bookmarks import Bookmarks
    from models.users import User

    queries_of_user = show_queries_in_my_account()

    bookmarks_of_user = []
    current_user_id = current_user.get_id()
    for user, bm in db.session.query(Bookmarks, User).filter(Bookmarks.user_id_bm == current_user_id).filter(
                    Bookmarks.user_id_bm == User.id):
        bookmarks_of_user.append(user.user_bookmark)

    return render_template('my_account.html', current_user_queries = queries_of_user, user_bm = bookmarks_of_user)



@app.route('/reset_password', methods=['POST'])
def reset_password_success():
    from models.users import reset_pass
    password_from_form_first = request.form['reset_password_first']
    password_from_form_second = request.form['reset_password_second']
    old_password = request.form['old_password']

    reset_pass(password_from_form_first, password_from_form_second, old_password)

    return render_template('my_account.html')


@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    from models.bookmarks import Bookmarks
    bookmark_from_form = request.form['bm']

    user_id = current_user.get_id()
    new_bookmark = Bookmarks(user_bookmark=bookmark_from_form, user_id_bm=user_id)
    db.session.add(new_bookmark)
    db.session.commit()
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    from models.users import save_user_to_db, crypt_password

    login_from_form = request.form['login']
    password_from_form = request.form['password']

    new_user = crypt_password(login_from_form, password_from_form)

    save_user_to_db(new_user)
    flash('User successfully registered')

    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    from models.users import verify_user

    login = request.form['login']
    password = request.form['password']
    verify_user(login, password)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/supersearch_rest/api/users', methods=['GET'])
def users_list():
    from models.users import User
    from models.queries import Queries

    list_users = []
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
            'count':count
        }

        list_queries = []
        count = 0
        list_users.append(current_user_json)

    return jsonify({'queries': list_users})


if __name__ == '__main__':
    app.run()