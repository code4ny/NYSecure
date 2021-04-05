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

    # locations_list is the list of all the possible location that they can report. 
    # Pulled from database?
    locations_list = ["Location 1", "Location 2", "Location 3"]  # example value
    return render_template("location_reporting.html", locations_list=locations_list)


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
    if "block" in  request.args:
        block = request.args["block"]
        print(block)
        return render_template("summary.html")
    else:
        data = [(2,1,"Science Block"), (100,4,"Admin Block")]
        return render_template("summary_block.html", datas=data)
    