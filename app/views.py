from app import app
from flask import render_template, redirect

@app.route('/')
def root():
    return redirect('/reporting')

@app.route("/reporting")
def reporting():
    return render_template("location_reporting.html")

@app.route("/summary")
def summary():
    return render_template("summary.html")
