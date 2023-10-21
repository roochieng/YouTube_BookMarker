from flask import render_template, request, url_for, flash, redirect
from models.base_model import RegistrationForm, LoginForm 
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app, db



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bookmarks", methods=['GET', 'POST'])
# @login_required
def bookmarks():
    return render_template("bookmarks.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account for email: {form.email.data} has been created!", "success")
        return redirect(url_for('home'))
    return render_template("signup.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)