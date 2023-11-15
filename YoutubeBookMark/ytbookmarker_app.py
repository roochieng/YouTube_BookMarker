from flask import render_template, request, url_for, flash, redirect
from models.base_model import (RegistrationForm, LoginForm, 
                                               UrlBookmark, Password_ResetForm,
                                               Request_Password_resetForm, BookmarkSearchForm)
from config import app, db, bcrypt, mail
from pytube import YouTube
from models.storage import User, BookMarks
from models.ytbookmarker import YouTubeBookMarker
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from elasticsearch import Elasticsearch


def get_current_user():
    return current_user

table_headers = ("Video Name", "Channel Name", "Date Bookmarked", "Delete Bookmark")
headers = ("Video Name", "Channel Name", "Date Bookmarked")


@app.route("/")
def landing():
    return render_template("landing_page.html")


@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/about")
def about():
    return render_template("about.html")


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
    return redirect(url_for('landing'))

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    current_user = get_current_user()
    last_five_bookmarks = BookMarks.query.filter_by(user_id=current_user.id).order_by(BookMarks.date_created.desc()).limit(5).all()
    return render_template("home.html", bookmarks=last_five_bookmarks, headers=headers)


@app.route("/bookmark", methods=['GET', 'POST'])
@login_required
def bookmark():
    current_user = get_current_user()
    form = UrlBookmark()
    if form.validate_on_submit():
        url = form.video_url.data
        action = 'Delete'
        if url:
            bookmarked = BookMarks.query.filter_by(user_id=current_user.id, 
                                                   video_url=url).all()
            if bookmarked:
                flash(f"""Warning! You cannot bookmark a duplicate video: {
                    YouTubeBookMarker(url).get_title()
                    }, search it in Dashboard.""", "danger")
            else:
                video = YouTubeBookMarker(url)
                video_name = video.get_title()
                channel_name = video.get_channel_name()
                if video_name != 'No video found.':
                    with app.app_context():
                        bookmark = BookMarks(video_url=url, video_name=video_name, 
                                             channel_name=channel_name, 
                                             date_created=datetime.utcnow(), 
                                             user_id=current_user.id, delete=action)
                        db.session.add(bookmark)
                        db.session.commit()
                    flash(f"Success! Bookmarked video with title: {video_name}! Check it on your Dashboard", 'success')
                else:
                    flash(f"Warninig! Please provide a valid YouTube video URL.", 'danger')
                return redirect(url_for('bookmark'))
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



def send_pass_reset_email(user):
    if current_user.is_authenticated:
        token = user.get_token()  # Generate the token for the user you are sending the email to
        with app.app_context():
            msg = Message(subject='Password Reset Request', sender=app.config.get("MAIL_USERNAME"),
                        recipients=[user.email]) 
            msg.body=f'''To reset your password, visit the following link: {url_for('reset_password',
                                                                                token=token, _external=True)}
            If you did not make this request, please ignore the email, and no changes will be made.'''
            mail.send(msg)



@app.route("/password_reset_request", methods=['GET', 'POST'])
def password_reset_request():
    current_user = get_current_user()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = Request_Password_resetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_pass_reset_email(user)
        flash("An email has been sent with password reset details", 'info')
        return redirect(url_for('login'))
    return render_template("password_reset_request.html", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    current_user = get_current_user()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash("Invalid or expired token", 'warning')
        return redirect(url_for('password_reset_request'))
    form = Password_ResetForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create an application context-----app.app_context().push()
        with app.app_context(): 
            user.password = hashed_pass
            db.session.commit()
        flash(f"Success! Password updated successfully", "success")
        return redirect(url_for('login'))
    return render_template("reset_password.html", form=form)
"""
@app.route('/search_video', methods=['GET', 'POST'])
@login_required
def search_video():
    search_form = BookmarkSearchForm()
    videos = BookMarks.query.filter_by(user_id=current_user.id).all()
    if search_form.validate_on_submit():
        with app.app_context(): 
            video_searched =  'Flask' #form.video.data
            videos = videos.filter(videos.video_name.like('%' + video_searched + '%'))
        return render_template("search_results.html")
    return render_template("layout.html", search_form=search_form, videos=videos, headers=table_headers)

"""

if __name__ == "__main__":
    app.run(debug=True)
