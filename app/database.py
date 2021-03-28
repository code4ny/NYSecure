import os
import requests
import json
from flask_login import UserMixin

# replace with the path of the database.
testing_database = 'https://api.airtable.com/v0/appt1zYKCcPRO3xQW/'
database_url = os.environ.get('DATABASE_URL', testing_database)
# Retrieve airtable api key from https://airtable.com/account, login with code4ny google account
airtablekey = os.environ.get('AIRTABLE_KEY', None)
class DataStore:

    def __init__(self):
        self.url = database_url
        self.headers = {"Authorization":  "Bearer " + airtablekey, "Content-Type" : "application/json"}
    
    def insert(self, table, record:dict):
        """
        Inserts record into table in database
        """
        upload_dict = {"records" : [{"fields": record}], "typecast": False}
        upload_json = json.dumps(upload_dict)
        response = requests.post(self.url + table, data=upload_json, headers=self.headers)

    def get_records(self, table):
        """
        Returns all records from table in a list of dicts
        """
        params = ()
        airtable_records = []
        run = True
        while run is True:
            response = requests.get(self.url + table, params=params, headers=self.headers)
            airtable_response = response.json()
            airtable_records += (x["fields"] for x in airtable_response["records"])
            if "offset" in airtable_response:
                run = True
                params = (("offset", airtable_response["offset"]),)
            else:
                run = False
        return airtable_records

    def get_records_by_param(self, table, params={}):
        """
        Returns all records from table in a list of dicts that fulfils params
        """
        response = requests.get(self.url + table, params=params, headers=self.headers)
        airtable_response = response.json()
        airtable_records = [x["fields"] for x in airtable_response["records"]]
        return airtable_records


    def delete(self, table, record):
        pass

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
            user = cls(usr["id"], usr["name"], usr["email"], usr["type"], usr["profile_pic"])
            return user
    
    def to_db(self, ds):
        """
        Inserts a row with name, email, type, and profile_pic into "users" table in database in a DataStore object.
        """
        ds.insert("users", {"id": self.id, "email": self.email, "name": self.name, "type": self.type, "profile_pic": self.profile_pic})