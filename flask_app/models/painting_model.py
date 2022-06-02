from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Painting:
    db = "final_exam_schema"
    def __init__(self, data):
        self.id = data["id"]

        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]
        
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]



    @staticmethod
    def validate_painting(form_data):
        is_valid = True

        if len(form_data["title"]) < 2:
            flash("Title name must be 2 characters long")
            is_valid = False

        if len(form_data["description"]) < 10:
            flash("Description must be 10 characters long")
            is_valid = False

        if len(form_data["price"]) <= 0:
            flash("Please enter a valid price")
            is_valid = False
            
        elif int(form_data["price"]) <= 0:
            flash("Price must be greater than 0")
            is_valid = False
         
           
        return is_valid





    @classmethod
    def get_all_paintings(cls):
        query = "SELECT paintings.id, paintings.title, users.first_name, users.last_name, users.id AS user_id FROM paintings LEFT JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        return results



    @classmethod
    def create_new_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, created_at, updated_at, user_id) VALUES (%(title)s, %(description)s, %(price)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results



    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s AND user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @classmethod
    def get_painting_by_id(cls, data):
        query = "SELECT paintings.id, paintings.title, paintings.description, paintings.price, paintings.created_at, paintings.updated_at, paintings.user_id, users.first_name, users.last_name FROM paintings LEFT JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
 

    @classmethod
    def edit_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = now() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results