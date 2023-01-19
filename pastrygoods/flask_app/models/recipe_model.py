from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.user_model import User


class recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.image = data['image']
        self.name = data['name']
        self.description = data['description']
        self.ingredient = data['ingredient']
        self.cook_time = data['cook_time']
        self.difficulty = data['difficulty']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ******* JOIN METHOD **********
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM Recipes JOIN Users ON recipes.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        list_recipes = []
        for row in results:
            current_recipe = cls(row)
            user_data ={
                ** row
                # 'id': row['users.id'],
                # 'created_at': row['users.created_at'],
                # 'updated': row['users.updated_at']
            }
            current_user = User(user_data)
            current_recipe.user = current_user 
            list_recipes.append(current_recipe)
        return list_recipes


# **********  CREATE RECIPE ********
    @classmethod
    def create(cls,data):
        query = 'INSERT INTO recipes(image,name, description,ingredient,cook_time,difficulty, user_id) VALUES (%(image)s,%(name)s, %(description)s, %(ingredient)s,%(cook_time)s, %(difficulty)s, %(user_id)s);'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


# ******** DELETE **********

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s" 
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
# ******* EDIT PAGE ********* 
    @classmethod
    def edit_recipe(cls,data):
        query = "Update Recipes SET name = (image, name, description, ingredient,cook_time,difficulty, user_id) VALUES (%(image)s,%(name)s, %(description)s, %(ingredients)s,%(cook_time)s, %(difficulty)s, %(user_id)s) WHERE Recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

# ******** GET ONE USER FOR RECIPE ************
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM Recipes JOIN Users ON Recipes.user_id = users.id WHERE Recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        list_recipes = []

        for row in results:
            current_recipe = cls(row)
            user_data ={
                ** row,
                # 'created_at' : row['Users.created_at'],
                # 'updated': row['Users.updated_at'],
                # 'id': row['users.id']
            }
            current_user =User(user_data)
            current_recipe.User = current_user 
            list_recipes.append(current_recipe)
        return list_recipes
        

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if data['image'] == '':
            flash('image must be filled', 'error_recipe_image')
            is_valid = False
        if data['name'] == '':
            flash('name must be filled', 'error_recipe_name')
            is_valid = False
        if data['description'] == '':
            flash('description must be filled', 'error_recipe_description')
            is_valid = False
        if data['ingredient'] == '':
            flash('ingredient must be filled', 'error_recipe_ingredient')
            is_valid = False
        if data['cook_time'] == '':
            flash('cook time must be filled', 'error_recipe_cook_time')
            is_valid = False
        if len (data['name']) < 3:
            flash("name must be at least 3 characters long", 'recipe_name')
            is_valid = False
        if len (data['description']) < 20:
            flash("description must be at least 20 characters long", 'error_recipe_description')
            is_valid = False
        if len (data['ingredient']) < 20:
            flash("ingredients must be at least 20 characters long", 'error_recipe_ingredient')
            is_valid = False

        return is_valid
