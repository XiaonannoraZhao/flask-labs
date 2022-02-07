import email
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired,ValidationError,EqualTo,Regexp, Length,Email
from flask_app.models import User
from flask_login import login_user, current_user, logout_user
import re


class RegistrationForm (FlaskForm):
  
    first_name_new = StringField(label="Username", validators = [DataRequired()])
    email_new= StringField(label='Email',validators=[DataRequired(),Regexp( r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message='Invalid email. Please check.')
    ])
    password_new = PasswordField("Password", validators = [DataRequired(),Regexp(r'^[A-Za-z0-9\s]*$', message='"Your password contain invalid characters.')
    ])
    password_confirm=PasswordField("Password", validators = [DataRequired(),EqualTo("password_new")])
    submit = SubmitField("Push me!")


    # for verifying repetitive registration by username
    # Code adaoted from stackbuse example:
    #  https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
    def validate_username(self, first_name_new):
        user = User.query.filter_by(username=first_name_new.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    # for verifying repetitive registration by email
    def validate_email(self, email_new):
        user = User.query.filter_by(email=email_new.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')
        mailRex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(mailRex,email_new) is None:
            print(email_new)
            raise ValidationError('Invalid email. Please check.')
   
   
    def validate_password(self, password_new):
      
         if password_new.data != self.password:
            user = User.query.filter_by(password=password_new.data).first()
            if user:
                 raise ValidationError('Passwords do not match. Please try again.')

class LoginForm(FlaskForm):
    email= StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    short_description = TextAreaField('Short_description', validators=[DataRequired(), Length(min=3, max=400)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SelectOrderForm(FlaskForm):
    date = SelectField('sort order', choices=['date_asc', 'date_desc'])
    vsubmit = SubmitField('Update')

class CommentForm(FlaskForm):

    comment = StringField("Content", validators=[DataRequired()], widget=TextAreaField("please add comment."))
    
    user_id= StringField("User")

    submit = SubmitField('Submit')