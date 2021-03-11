import os

# replace with the path of the database.
testing_database = ''
database_url = os.environ.get('DATABASE_URL', testing_database)