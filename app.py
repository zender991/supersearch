from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, g
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


@login_manager.user_loader
def load_user(id):
    return Bratuha.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')



@app.route('/results', methods=['POST'])
@login_required
def show():
    form_query = request.form['title']
    youtube_videos = youtube_search(form_query)

    youtube_videos_json = json.dumps(youtube_videos)

    youtube_videos_list = json.loads(youtube_videos_json)

    list_tweets = twitter_search(form_query)

    twitter_json = json.dumps(list_tweets)

    twitter_list_template = json.loads(twitter_json)

    #print(list_tweets)


    return render_template('results.html', yt_vid = youtube_videos_list, tweets = twitter_list_template)
    #return render_template('results.html', tweets=list_tweets)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = Bratuha(request.form['login'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
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



if __name__ == '__main__':
    app.run()