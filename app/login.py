import json
import os
import requests

from flask import redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
from app.database import DataStore, User
from app import app

a = DataStore()
# Retrieve client id and secret from https://console.cloud.google.com/apis/credentials?project=nysecure
# Login with code4ny google account
google_client_id = os.environ.get("GOOGLE_CLIENT_ID", None)
google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", None)
google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    return requests.get(google_discovery_url).json()


login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(google_client_id)


@login_manager.user_loader
def load_user(user_id):
    return User.get(a, user_id)


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
        hd="nyjc.edu.sg",
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    usrinfodict = userinfo_response.json()
    if usrinfodict.get("email_verified"):
        unique_id = usrinfodict["sub"]
        users_email = usrinfodict["email"]
        picture = usrinfodict["picture"]
        users_name = f"{usrinfodict['given_name']} {usrinfodict['family_name']}"
    else:
        return "User email not available or not verified by Google.", 400

    # Assigns a type to the user and creates user object
    if "Staff" in users_name:
        type_ = "staff"
    else:
        type_ = "student"

    # Additional check for nyjc account
    domain = users_email.split("@")[1]
    if domain != "nyjc.edu.sg":
        return redirect(url_for("root"))
    else:
        user = User(unique_id, users_name, users_email, type_, picture)

        # Adds user to database if it does not exist
        if User.get(a, unique_id) is None:
            user.to_db(a)

        login_user(user, remember=True)
        return redirect(url_for("root"))  # redirect after the login


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("root"))


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
