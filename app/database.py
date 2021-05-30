"""DataStore and User class to work with the database and any other function to manipulate it."""

import os
import requests
import json
from flask_login import UserMixin
import psycopg2
from app.config import DATABASE_URI
import psycopg2.extras

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
        conn = self.get_connection()
        cur = conn.cursor()

        if block is None and level is None:
            cur.execute("SELECT LocationName FROM Location;")
        elif block is not None and level is None:
            cur.execute("SELECT LocationName FROM Location WHERE Block=%s;", (block,))
        elif block is None and level is not None:
            cur.execute("SELECT LocationName FROM Location WHERE Level=%s;", (level,))
        else:
            cur.execute("SELECT LocationName FROM Location WHERE BLOCK=%s AND Level=%s;", (block, level))

        result = cur.fetchall()
        return [row[0] for row in result]

    def get_summary(self, block=None, level=None):
        """Return all the locations with their associated number of people there.

        Filtered based on condition.

        Args:
            block (str, optional): Locations with that block. Defaults to None, which will return all.
            level (int, optional): The level of the location. Defaults to None, which will return all.

        Returns:
            dict: Contains all the required values. If invalid filter, return None.
        """
        conn = self.get_connection()
        cur = conn.cursor()

        resultlist = []
        locations = self.get_locations_list(block, level)
        locationpax_dict = dict()
        
        for location in locations:
            locationpax_dict[location] = 0

        cur.execute('''SELECT DISTINCT ON (UserID) Location,ReportingTime,UserID,Pax 
                    FROM (SELECT * FROM Report ORDER BY ReportingTime DESC) as foo;''')
        result = cur.fetchall()

        filtered = []

        for index, row in enumerate(result):
            if row[0] in locations:
                filtered.append(row)
        
        for row in filtered:
            locationpax_dict[row[0]] += 1
        
        if len(locationpax_dict) < 1:
            return None
            
        return locationpax_dict

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

    def insert_user(self, userdict):
        """
        Inserts a row into the user table

        Args:
            userdict (dict): dict containing userid, email, name, type and profilepic of the user
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
        INSERT INTO users (userid, email, name, type, profilepic)
        VALUES (%s,%s,%s,%s,%s);
        """,
            (
                userdict["id"],
                userdict["email"],
                userdict["name"],
                userdict["type"],
                userdict["profile_pic"],
            ),
        )
        conn.commit()
        conn.close()

    def get_user(self, userid):
        """
        Selects user from users table with userid

        Args:
            userid (str): Unique Google assigned userid

        Returns:
            psycopg2.extras.RealDictRow: Dict-like object with information of user
        """
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
        SELECT * FROM users
        WHERE userid = %s;
        """,
            (userid,),
        )
        result = cur.fetchone()
        conn.close()
        return result


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
        Constructor method that creates its User class from user_id in a DataStore ds

        Args:
            ds (DataStore): DataStore object to retrieve user info from
            user_id (str): Unique Google assigned userid

        Returns:
            None/User: Returns an instance of its class if the user with user_id exists, else returns None
        """
        usr = ds.get_user(user_id)
        if usr is None:
            return None
        else:
            user = cls(
                usr["id"], usr["name"], usr["email"], usr["type"], usr["profilepic"]
            )
            return user

    def to_db(self, ds):
        """
        Inserts a row with name, email, type, and profile_pic into table in database in a DataStore object,
        from the attributes in self.

        Args:
            ds (DataStore): DataStore object to insert data into
        """
        ds.insert_user(
            {
                "id": self.id,
                "email": self.email,
                "name": self.name,
                "type": self.type,
                "profile_pic": self.profile_pic,
            },
        )
