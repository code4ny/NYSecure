import os

from flask import Flask
from flask_talisman import Talisman

from app.config import CONTENT_SECURITY_POLICY

app = Flask(__name__)

# view https://github.com/GoogleCloudPlatform/flask-talisman for documentations
Talisman(
    app,
    force_https=True,  # Ensure that url uses https for google login
    force_https_permanent=True,  # show that url has permanent relocation
    content_security_policy=CONTENT_SECURITY_POLICY
)

app.secret_key = os.environ.get("app_secret_key", os.urandom(24))

from app import views
from app import api
from app import login
