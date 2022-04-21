import this
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    db = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date = data['date']
        self.under_30_mins = data['under_30_mins']
        self.created_at = data['created_at']
        self.updated_on = data['updated_at']
        self.user_id = data['user_id']
        self.likes = []

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data["name"]) <= 3:
            flash("Recipe Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data["description"]) <= 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data["instruction"]) <= 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        if len(data['date']) == 0:
            flash("Please select the date", "recipe")
            is_valid = False
        if data['under_30_mins'] == "":
            flash("Please select if the recipe is under 30 mins or not", "recipe")
            is_valid = False
        return is_valid

    @classmethod
    def getall_recipes(cls):
        query= "SELECT * from recipes;"
        results = MySQLConnection(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one_recipe(cls,data):
        query= "SELECT * from recipes WHERE id = %(id)s;"
        results = MySQLConnection(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, date, under_30_mins, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date)s, %(under_30_mins)s, %(user_id)s);"
        return MySQLConnection(cls.db).query_db(query,data) #method returns users.id from database

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description = %(description)s, instruction=%(instruction)s, date=%(date)s, under_30_mins=%(under_30_mins)s WHERE id= %(id)s;"
        return MySQLConnection(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE from recipes WHERE id = %(id)s"
        return MySQLConnection(cls.db).query_db(query,data)
    
    @classmethod
    def get_user_from_recipe(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        result = MySQLConnection(cls.db).query_db(query,data)
        print(result[0])
        return result[0]
    
    @classmethod
    def save_likes(cls,data):
        query = "INSERT into likes (recipes_id, likeby_users_id) VALUES (%(recipes_id)s,%(likeby_users_id)s);"
        return MySQLConnection(cls.db).query_db(query,data)

    @classmethod
    def remove_likes(cls,data):
        query = "DELETE FROM likes WHERE recipes_id = %(recipes_id)s and likeby_users_id = %(likeby_users_id)s;"
        return MySQLConnection(cls.db).query_db(query,data)

    # using this method is more efficient and we don't need "getall_recipes" method because it gets "all the recipes" and "recipes.likes" both
    @classmethod
    def get_likes(cls):
        query = "SELECT * FROM recipes left join likes ON recipes.id = likes.recipes_id;"
        results= MySQLConnection(cls.db).query_db(query)
        print(f"{results}")
        recipes  = []
        for row in results:
            likes_info = {
                "recipes_id": row['recipes_id'],
                "likeby_users_id": row['likeby_users_id']
            }
            if len(recipes) > 0 and recipes[len(recipes)-1].id == row['id']:
                if row["recipes_id"] != None:
                    recipes[len(recipes)-1].likes.append(likes_info)
            else: 
                this_recipe = cls(row)
                if row["recipes_id"] != None:
                    this_recipe.likes.append(likes_info)
                recipes.append(this_recipe)
        return recipes


