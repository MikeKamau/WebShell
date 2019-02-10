from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.urls import url_parse
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegisterForm, LoginForm, CommandForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import subprocess


#Initialization of the application setiings and related settings
app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "l\xf6\xa4\xd4\xb8\xaf\x10\xb1\xb5\xf0j\xa7\xa5\xf1q\n6Mz\xf6T\xa3GjB]A\xa8\xc5\xf2\x05\x1d"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/webshell'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
from models import User, Command


#The index view
@app.route('/')
def index():
    return render_template("home.html")


#The command view, that takes the commands to be run from the user and submits them to the backend shell
@app.route('/command', methods=['GET','POST'])
@login_required
def command():
    form = CommandForm()
    if form.validate_on_submit():
        command = form.command_input.data
        cmd = Command(command=command, user_id=session['user_id'])
        db.session.add(cmd)
        db.session.commit()
        return redirect(url_for('view', cmd_string=command))
    return render_template("command.html", form=form)


#The login view to handle the login functionality
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        session['user_id'] = user.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash("You're now logged in")
            return redirect(url_for('index'))
        flash("You're now logged in")
        return redirect(next_page)
    return render_template("login.html", form=form)


#The riegistration view
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congragulations your registration was successful')
        return redirect(url_for('login'))
    return render_template("login.html", form=form)


#Logout view
@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))


#Display view that displays the output of running commands submitted in the "command" view
@app.route('/view')
@login_required
def view():
    cmd = request.args.get('cmd_string')
    cmd_list = cmd.strip().split()
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    command_output = process.stdout.readlines()
    return render_template("view.html", output=command_output)


#View that displays the commands that a user submitted previously
@app.route('/submitted')
@login_required
def submitted():
    user_id = session['user_id']
    commands_submitted = Command.query.filter_by(user_id=int(user_id))
    return render_template("submitted.html", cmds=commands_submitted)


if __name__ == "__main__":
    app.run()
