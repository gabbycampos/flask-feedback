from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, DataRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please enter a username")])
    password = PasswordField("Password", validators=[InputRequired("Please enter a password")])
    email = StringField("Email Address", validators=[DataRequired("Please enter your email address")])
    first_name = StringField("First name", validators=[InputRequired("Please enter your first name")])
    last_name = StringField("Last name", validators=[InputRequired("Please enter your last name")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please enter your name")])
    password = PasswordField("Password", validators=[InputRequired("Please enter your password")])

class AddFeedBackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Please enter the title of feedback")])
    content = TextAreaField("Content", validators=[InputRequired("Please enter missing comment")])