"""To render the html files for viewing.

Database processing should be done in the the `database.py` file as much as possible.
"""
from time import sleep

from flask import render_template, redirect, request, make_response
from flask.helpers import url_for

from app import app
from app.database import DataStore
from app.login import current_user

ds = DataStore()


@app.route("/")
def root():
    """To check with the user is login, and log them in if necessary.

    Otherwise, redirect to the reporting page.
    """
    sleep(2)  # to give time to authenticate
    if current_user.is_authenticated:
        return redirect(url_for("reporting"))
    else:
        return render_template("index.html")


@app.route("/reporting")
def reporting():
    """
    Display the form.

    Returns:
        render_template("location_reporting.html")
    """
    # locations_list is the list of all the possible location that they can report.
    locations_list = ds.get_locations_list()
    lastReportedLoc = request.cookies.get("lastReportedLoc", None)
    lastReportedTime = request.cookies.get("lastReportedTime", None)
    haveSubmitted = bool(request.cookies.get("haveSubmitted", False))
    return render_template(
        "location_reporting.html",
        current_user=current_user,
        locations_list=locations_list,
        haveSubmitted=haveSubmitted,
        lastReportedLoc=lastReportedLoc,
        lastReportedTime=lastReportedTime,
    )


@app.route("/update", methods=["POST"])
def update():
    """
    Update the database based on the location being reported.

    Returns:
        redirect("reporting")
    """
    location = request.form.get("location")
    userid = request.form.get("current_user_id")
    current_time = request.form.get("current_time")
    if userid is not None:
        ds.update_report(userid, location)
        resp = make_response(redirect("/reporting"))
        resp.set_cookie("lastReportedLoc", location)
        resp.set_cookie("lastReportedTime", current_time)
        resp.set_cookie("haveSubmitted", 1)
        return resp
    else:
        resp = make_response(
            'Please try again! <br /><a href="/reporting">return back</a>'
        )
        resp.set_cookie("haveSubmitted", 0)
        return resp


@app.route("/summary")
def summary():
    """
    Show the blocks and number of students.
    """
    return render_template("summary.html")
