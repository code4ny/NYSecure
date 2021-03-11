from app import app
from flask import render_template, redirect, request

@app.route('/')
def root():
    """Does nothing for now.

    Returns:
        redirect to the reporting page
    """
    return redirect('/reporting')


@app.route("/reporting")
def reporting():
    """
    Displays the form. Redirects to update

    Returns:
        render_template("location_reporting.html")
    """
    
    return render_template("location_reporting.html")


@app.route("/update")
def update():
    """    
    Update the database based on the location being reported.

    Returns:
        redirect("reporting")
    """

    return redirect("/reporting")


@app.route("/summary")
def summary():
    """
    Shows the blocks and number of students

    Returns:
        render_template("summary.html")
    """

    return render_template("summary.html")
    