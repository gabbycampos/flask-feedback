from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, AddFeedBackForm
from sqlalchemy.exc import IntegrityError

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

# @app.route('/secret')
# def show_secret():
#     if "user_id" not in session:
#         flash('Please login first')
#         return redirect('/')
#     return render_template('secret.html')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data 
        last_name = form.last_name.data 

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form, button='Register')
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f'/users/{new_user.id}')
    return render_template('register.html', form=form, button='Register')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 

        user = User.authenticate(username, password)
        
        if user:
            flash(f"Welcome Back, {user.username}!", 'info')
            session['user_id'] = user.id
            return redirect(f'/users/{user.id}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form, button='Login')

@app.route('/logout')
def logout():
    """ Log out user """
    session.pop('user_id')
    flash('Goodbye!')
    return redirect('/')

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """ user info """
    if 'user_id' not in session:
        flash('Please login first')
        return redirect('/login')
    user = User.query.get_or_404(user_id)
    feedbacks = db.session.query(Feedback).filter_by(user_id=user_id).all()
    return render_template('user_info.html', user=user, feedbacks=feedbacks)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect('/login')
    form = LoginForm()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')
    flash('Account was deleted', 'warning')
    return redirect('/login')

@app.route('/users/<int:user_id>/feedback/add', methods=["GET", "POST"])
def add_feedback(user_id):
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect('/login')
    form = AddFeedBackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data 
        feedback = Feedback(title=title, content=content, user_id=user_id)
        db.session.add(feedback)
        db.session.commit()
        flash("Your feedback was added")
        return redirect(f'/users/{user_id}')
    return render_template('add_feedback.html', form=form, button="submit")

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    form = AddFeedBackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data 
        feedback.content = form .content.data
        db.session.commit()
        flash("Feedback updated successfully", "info")
        return redirect(f'/users/{session["user_id"]}')
    return render_template('update_feedback.html', button='Update', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    if session.get("user_id"):
        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted", "info")
        return redirect(f'/users/{session["user_id"]}')
    else:
        flash("Please login first!", "danger")
        return redirect('/login')