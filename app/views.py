"""To render the html files for viewing.

Any heavy logic processing should be done in a separate file as much as possible.
"""

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
    lastReportLoc = request.cookies.get("lastReportedLoc", None)
    lastReportTime = request.cookies.get("lastReportedTime", None)
    haveSubmitted = bool(request.cookies.get("haveSubmitted", False))
    last_submitted_message = (
        f"Your last reported location is {lastReportLoc} on {lastReportTime}"
        if haveSubmitted
        else "You haven't reported!"
    )
    return render_template(
        "location_reporting.html",
        current_user=current_user,
        locations_list=locations_list,
        last_submitted_message=last_submitted_message,
    )


@app.route("/update", methods=["POST"])
def update():
    """
    Update the database based on the location being reported. And set cookies.


    Returns:
        redirect("reporting")
    """
    location = request.form.get("location")
    userid = request.form.get("current_user_id")
    current_time = request.form.get("current_time")
    if userid is not None:
        # Updating the Database
        ds.update_report(userid, location)

        # Update the cookies
        resp = make_response(redirect("/reporting"))
        resp.set_cookie("lastReportedLoc", location)
        resp.set_cookie("lastReportedTime", current_time)
        resp.set_cookie("haveSubmitted", "True")
        return resp
    else:
        resp = make_response(
            'Please try again! <br /><a href="/reporting">return back</a>'
        )
        resp.set_cookie(
            "haveSubmitted", "", expires=0
        )  # cookies immediately expires, equivalent to deleting
        return resp


@app.route("/summary")
def summary():
    """
    Show the blocks and number of students.
    """

    authenticated = current_user.type == "staff" or (
        request.args.get("debug", "") == "yes"
    )

    return render_template(
        "summary.html", current_user=current_user, authenticated=authenticated
    )
