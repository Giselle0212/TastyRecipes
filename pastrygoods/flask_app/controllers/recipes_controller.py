from flask_app import app
from flask import render_template, request, redirect,flash, session
from flask_app.models.recipe_model import recipe
from flask_app.models.user_model import User


# ********CREATING A RECIPE********
@app.route('/create/recipe')
def  create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add.html')


# **********SUBMIT ACTIONS *************
@app.route('/new/recipes', methods =["POST"] )
def new_recipe():
    # print("****** valid *******");
    if recipe.validate_recipe(request.form) == False:
        return redirect('/create/recipe')
    data = {
        ** request.form,
        'user_id': session['user_id']
    }
    # print(users_id,"******* valid ********");
    # print(session['user_id']," *** 123 ***")
    recipe.create(data)
    return redirect('/post')


# ******** VIEW RECIPE ********
@app.route('/view/<int:id>')
def display_one(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    current_recipe = recipe.get_one_user(data)
    return render_template('view.html', current_recipe = current_recipe)
    
# ********* EDIT PAGE *********
@app.route('/update/<int:id>')
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    current_recipe =recipe.get_one_user(data)
    return render_template('edit.html', current_recipe = current_recipe)

@app.route('/process_edit/<int:id>', methods = ['POST'])
def process_recipe(id):
    if recipe.validate_recipe(request.form) == False:
        return redirect(f'/edit/{id}')
    data = {
        "id": id,
        "image": request.form["image"],
        "name": request.form["name"],
        "description": request.form["description"],
        "ingredient": request.form["ingredient"],
        "cook_time": request.form["cook_time"],
        "difficulty": request.form["difficulty"],
        "user_id": session['user_id']
    }
    recipe.edit_recipe(data) 
    return redirect('/post')
# ********** DELETE ***********
@app.route('/delete/<int:id>')
def process_delete(id):
    data={
        'id': id
    }
    recipe.delete_recipe(data) 
    return redirect('/post')