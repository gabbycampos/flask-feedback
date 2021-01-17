from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedbacksecreteapp"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/secret')
def show_secret():
    return render_template('secret.html')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.username.data
        email = form.username.data
        first_name = form.username.data 
        last_name = form.username.data 

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        flash('Welcome! Successfully Created Your Account!')
        return redirect('/secret')

    return render_template('register.html', form=form, button='Register')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 

        user = User.authenticate(username, password)
        
        if user:
            flash("Welcome Back, {user.username}!")
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form, button='Login')

@app.route('/logout')
def logout():
    """ Log out user """
    session.pop('user_id')
    flash('Goodbye!')
    return redirect('/')