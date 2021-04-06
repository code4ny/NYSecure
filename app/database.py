"""
DataStore class to work with the database and any other function to manipulate it
"""

import os
import requests
import json
from flask_login import UserMixin
import psycopg2
from app.config import DATABASE_URI


class DataStore:
    def __init__(self):
        # FOR TESTING, TO BE REPLACED!
        testing_database = DATABASE_URI
        self.url = os.environ.get("DATABASE_URL", testing_database)

    def get_connection(self):
        return psycopg2.connect(self.url)


class User(UserMixin):
    def __init__(self, id_, name, email, type_, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.type = type_
        self.profile_pic = profile_pic

    @classmethod
    def get(cls, ds, user_id):
        """
        Returns a User object from a DataStore object, whose id is user_id.
        Returns None if user does not exist in DataStore.
        """
        usr = ds.get_records_by_param("users", {"filterByFormula": f"id={user_id}"})
        if len(usr) == 0:
            return None
        else:
            usr = usr[0]
            user = cls(
                usr["id"], usr["name"], usr["email"], usr["type"], usr["profile_pic"]
            )
            return user

    def to_db(self, ds):
        """
        Inserts a row with name, email, type, and profile_pic into "users" table in database in a DataStore object.
        """
        ds.insert(
            "users",
            {
                "id": self.id,
                "email": self.email,
                "name": self.name,
                "type": self.type,
                "profile_pic": self.profile_pic,
            },
        )
