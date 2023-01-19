from flask_app import app
from flask import render_template, request, redirect,session,flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import recipe

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
#  ***** HOME PAGE ****
@app.route('/')
def index():
    return render_template('login_reg.html')

#  ****** LOGIN & REG ***** 
@app.route('/login/reg')
def login_reg():
    return render_template('login_reg.html')
    

#  **** POST *********
@app.route('/post')
def post():
    if  'user_id' not in session:
        return redirect('/')
    list_recipes = recipe.get_all_recipes()
    return render_template('post.html', list_recipes = list_recipes)


# ***** Registration ********
@app.route('/user/register', methods=['POST'])
def register():
    if not User.validator(request.form):
        return redirect('/login/reg')
    data = {
        **request.form,
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.create(data)
    #  *** possible bug *** 
    session['user_id'] = user_id
    # print("this is the id" , id)
    #  *** possible bug *** 
    return redirect('/post')


# ******* Login *********
@app.route('/user/login', methods=['POST'])
def login():
    login_user = User.get_by_email(request.form)
    if not login_user:
        flash('invalid', 'error_login_credentials')
        return redirect('/login/reg')
    if not bcrypt.check_password_hash(login_user.password, request.form['password']):
        flash('invalid', 'error_login_credentials')
        return redirect('/login/reg')

    session['first_name'] = login_user.first_name
    session['user_id'] = login_user.id
    return redirect('/post')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login/reg')

@app.route('/add')
def add():
    return render_template('add.html')