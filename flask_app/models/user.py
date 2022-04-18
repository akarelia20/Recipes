from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data["first_name"]) <= 1:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if len(data["last_name"]) <= 1:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be atleast 8 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False 
            flash("Invalid email address!", "register")
        if data['password'] != data['confirm_password']:
            is_valid = False 
            flash("Passwords do not match, try entering it again", "register")
        
        query = "SELECT * FROM users where email = %(email)s"
        result= connectToMySQL(User.db).query_db(query,data)
        if len(result) >= 1:
            is_valid = False
            flash('Email already exist in database!!', "register")
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return MySQLConnection(cls.db).query_db(query,data) #method returns users.id from database

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL(User.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users where email= %(email)s;"
        results = connectToMySQL(User.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])