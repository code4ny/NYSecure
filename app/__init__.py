from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get("app_secret_key", os.urandom(24))

from app import views
from app import api
from app import login
