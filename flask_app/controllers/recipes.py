from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe, user

@app.route("/recipe/new")
def newrecipe():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    logged_user = user.User.get_user_by_id(data)
    return render_template("create_recipe.html", user = logged_user)

@app.route("/recipe/create", methods =['POST'])
def create_recipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/recipe/new")
    else: 
        data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date": request.form['date'],
        "under_30_mins": request.form['under_30_mins'],
        "user_id" : session['user_id']
        }
        recipe.Recipe.save(data)
        return redirect("/dashbord")

@app.route("/recipe/<int:id>")
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    data2 = {
        "id" : session['user_id']
    }
    return render_template("view_recipe.html", recipe = recipe.Recipe.get_one_recipe(data), logged_in_user = user.User.get_user_by_id(data2), user = recipe.Recipe.get_user_from_recipe(data))

@app.route("/recipe/edit/<int:id>")
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data= {
        "id" : id
    }
    data2 = {
        "id" : session['user_id']
    }
    return render_template("edit_recipe.html", recipe = recipe.Recipe.get_one_recipe(data), logged_in_user = user.User.get_user_by_id(data2))

@app.route('/recipe/update/<int:id>', methods=["POST"])
def update_recipe(id):
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f"/recipe/edit/{id}")
    else: 
        data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "instruction": request.form['instruction'],
            "date": request.form['date'],
            "under_30_mins": request.form['under_30_mins'],
            "id": id
        }
        recipe.Recipe.update(data)
        return redirect(f"/recipe/{id}")

@app.route("/recipe/like/<int:id>")
def like_recipe(id):
    data = {
        "recipes_id" : id,
        "likeby_users_id" : session["user_id"]
    }
    recipe.Recipe.save_likes(data)
    return redirect("/dashbord")

@app.route('/recipe/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data= {
        "id" : id
    }
    recipe.Recipe.delete(data)
    return redirect ('/dashbord')





