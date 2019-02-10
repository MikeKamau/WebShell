from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots or '
        'underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), ])
    submit = SubmitField('Register')


    def validate_username(self, username):
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken, please use a different username')

    def validate_email(self, email):
        from models import User
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Username already taken, please use a different address')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots or '
        'underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class CommandForm(FlaskForm):
    command_input = StringField('Bash Command', validators=[DataRequired()])
    submit = SubmitField('Run Command')
