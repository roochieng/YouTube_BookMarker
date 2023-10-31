from flask import render_template, request, url_for, flash, redirect
from YoutubeBookMark.models.base_model import RegistrationForm, LoginForm, UrlBookmark
from flask_sqlalchemy import SQLAlchemy
from YoutubeBookMark.config import app, db, bcrypt
from pytube import YouTube
from YoutubeBookMark.models.storage import User, BookMarks
from YoutubeBookMark.models.ytbookmarker import YouTubeBookMarker
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


def get_current_user():
    return current_user

table_headers = ("Video Name", "Channel Name", "Date Bookmarked", "Delete Bookmark")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def bookmarks():
    current_user = get_current_user()
    user_bookmarks = BookMarks.query.filter_by(user_id=current_user.id).all()
    return render_template("bookmarks.html", bookmarks=user_bookmarks, table_headers=table_headers)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    headers = ("Video Name", "Channel Name", "Date Bookmarked")
    current_user = get_current_user()
    last_five_bookmarks = BookMarks.query.filter_by(user_id=current_user.id).order_by(BookMarks.date_created.desc()).limit(5).all()
    return render_template("home.html", bookmarks=last_five_bookmarks, headers=headers)


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/bookmark", methods=['GET', 'POST'])
@login_required
def bookmark():
    current_user = get_current_user()
    form = UrlBookmark()
    if form.validate_on_submit():
        url = form.video_url.data
        action = 'Delete'
        if url:
            bookmarked = BookMarks.query.filter_by(user_id=current_user.id, video_url=url).all()
            if bookmarked:
                flash(f"Warning! You cannot bookmark a duplicate video: {YouTubeBookMarker(url).get_title()}.", "danger")
            else:
                video = YouTubeBookMarker(url)
                video_name = video.get_title()
                channel_name = video.get_channel_name()
                if video_name != 'No video found.':
                    with app.app_context():
                        bookmark = BookMarks(video_url=url, video_name=video_name, channel_name=channel_name, date_created=datetime.utcnow(), user_id=current_user.id, delete=action)
                        db.session.add(bookmark)
                        db.session.commit()
                    flash(f"Success! Bookmarked video with title: {video_name}! Check it on your Dashboard", 'success')
                else:
                    flash(f"Warninig! Please provide a valid YouTube video URL.", 'danger')
    return render_template("bookmark.html", form=form)


@app.route("/demo", methods=['GET', 'POST'])
def demo():
    return render_template('demo.html')

@app.route("/delete/<int:bookmark_id>", methods=['GET', 'POST'])
def delete(bookmark_id):
    with app.app_context():
        bookmark = db.session.query(BookMarks).filter_by(id=bookmark_id).first()
        if bookmark:
            db.session.delete(bookmark)
            db.session.commit()
            flash("Bookmark deleted successfully", 'success')
    return redirect(url_for('bookmarks'))


if __name__ == "__main__":
    app.run(debug=True)
