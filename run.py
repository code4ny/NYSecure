"""To run the flask app"""

from app import app

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
