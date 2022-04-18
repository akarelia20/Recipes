from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ['POST'])
def register():
    if not user.User.validate_registration(request.form):
        flash('Please login')
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash,
    }
    user_id = user.User.save(data) 
    session['user_id'] = user_id
    return redirect ("/dashbord")

@app.route("/login", methods= ['Post'])
def login():
    data = {
        "email": request.form['email']
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db: 
        flash("Invalid Email/Password !", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect("/")

    session['user_id'] = user_in_db.id
    return redirect("/dashbord")

@app.route("/dashbord")
def dashbord():
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : session['user_id']
    }
    all_recipes = recipe.Recipe.get_likes()
    # likes = recipe.Recipe.get_likes(data)
    return render_template("dashbord.html",logged_in_user = user.User.get_user_by_id(data), recipes = all_recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")