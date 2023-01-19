from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO users(first_name, last_name, email, password) VALUE (%(first_name)s,%(last_name)s, %(email)s, %(password)s); '
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            login_user = cls(result[0])
            return login_user
        else:
            return False




    @staticmethod
    def validator(user):
        is_valid =True
        if len(user['first_name']) < 3:
            flash('First Name is required', 'First_name_reg')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last Name is required', 'Last_name_reg')
            is_valid = False
        if len(user['email']) < 3:
            flash('Invalid Email', 'email_reg')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash('Email must be valid', ' reg')
            is_valid = False
        else:
            data ={
                'email': user['email']
            }
            user_in_db = User.get_by_email(data)
            if  user_in_db:
                flash('Email already registed', 'email_reg')
        if len(user['password']) < 8:
            flash('password must be 8 charactecters', 'password_reg')
            is_valid = False
        elif user['password'] != user['confirm_password']:
            flash('Password those not match', 'confirm_password_reg')
            is_valid = False
        return is_valid




