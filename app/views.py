"""To render the html files for viewing.

Database processing should be done in the the `database.py` file as much as possible.
"""

from app import app
from flask import render_template, redirect, request

# from flask_login import current_user
from app.database import DataStore
from app.login import current_user

ds = DataStore()


@app.route("/")
def root():
    """To check with the user is login, and log them in if necessary.

    Otherwise, redirect to the reporting page.
    """
    ds.get_connection()
    return render_template("index.html")
    # if current_user.is_authenticated:
    #     return render_template(
    #         "index.html", authenticated=True, current_user=current_user
    #     )
    # else:
    #     return render_template("index.html", authenticated=False)


@app.route("/reporting")
def reporting():
    """
    Display the form.

    Returns:
        render_template("location_reporting.html")
    """
    # locations_list is the list of all the possible location that they can report.
    locations_list = ds.get_locations_list()
    if current_user.is_authenticated:
        return render_template(
            "location_reporting.html", authenticated=True, current_user=current_user
        )
    else:
        return render_template("location_reporting.html", authenticated=False)
    # return render_template("location_reporting.html", locations_list=locations_list)


@app.route("/update")
def update():
    """
    Update the database based on the location being reported.

    Returns:
        redirect("reporting")
    """
    userid = None  # TODO: Ryan&JianSan
    assert False, "userid to be corrected. DELETE line when done!"
    location = request.form.get("location")
    ds.update_report(userid, location)
    return redirect("/reporting")


@app.route("/summary")
def summary():
    """
    Show the blocks and number of students.
    """
    return render_template('summary.html')
