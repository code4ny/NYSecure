"""DataStore and User class to work with the database and any other function to manipulate it."""

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
        """Return a connection to database.

        Returns:
            psycopg2.extensions.connection: connection to the database
        """
        return psycopg2.connect(self.url)

    def get_locations_list(self, block=None, level=None):
        """Return all the location in the school.

        Allow filtering of location

        Args:
            block (str, optional): Block to select. Defaults to None, which selects all.
            level (str, optional): Level to select. Defaults to None, which select all.

        Returns:
            list: list of location string
        """
        # TODO: Backend
        raise NotImplementedError

    def get_summary(self, block=None, level=None):
        """Return all the locations with their associated number of people there.

        Filtered based on condition.

        Args:
            block (str, optional): Locations with that block. Defaults to None, which will return all.
            level (int, optional): The level of the location. Defaults to None, which will return all.

        Returns:
            list: Contains all the required values. If invalid filter, return empty list.
        """
        # TODO: Backend
        raise NotImplementedError

    def update_report(self, userid, location, pax=1):
        """Update the report based on form submission.

        Args:
            userid (str): userid of person who submit the form.
            location (str): Location name string
            pax (int, optional): The number of people at the location. Defaults to 1.

        Returns:
            str/int: Denote whether the update was sucessful. If not success, the reason why. Similar to status code 200,404 etc.
        """
        # TODO: Backend
        raise NotImplementedError


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
