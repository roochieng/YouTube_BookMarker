from flask import render_template, request, url_for, flash, redirect
from models.base_model import RegistrationForm, LoginForm, UrlBookmark
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app, db, bcrypt
from pytube import YouTube
from models.storage import User
from models.ytbookmarker import YouTubeBookMarker
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def bookmarks():
    return render_template("bookmarks.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template("login.html", titel='login', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create an application context-----app.app_context().push()
        with app.app_context():
            user = User(email=form.email.data, password=hashed_pass, date_created=datetime.utcnow())
            db.session.add(user)
            db.session.commit()
        flash(f"Account for email: {form.email.data} has been created!", "success")
        return redirect(url_for('login'))
    return render_template("signup.html", title='Register', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template("index.html")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/bookmark", methods=['GET', 'POST'])
def bookmark():
    form = UrlBookmark()
    url = form.url.data
    if url:
        video = YouTubeBookMarker(url)
        video_name = video.get_title()
        channel_name = video.get_channel_name()
        with app.app_context():
            bookmark = UrlBookmark(video_url=url, video_name=video_name, channel_name=channel_name, date_created=datetime.utcnow())
        flash(f"You have book marked video link with title: {video_name}! check it on bookmarks", 'success')
    else:
        flash("Please provide a valid URL.", 'danger')
    return render_template("bookmark.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
