# Title: Application for Data Science Job-Application Capstone
# Purpose: To create an application to display jobs and market-related info to a employer
# Created by: Saani Rawat
# Last modifed: 04/29/2020
# Input:
# 1. web_scraping_stock_data.py
# Output:
# Stock Price Application

from flask import Flask, render_template, request, redirect, url_for
import os
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

@app.route('/')
def show():
    # return "Hello, world."
    return render_template("home.html")



@app.route('/submit', methods = ['POST'])
def submit():
    # return "This is another page of the website"
    # return render_template("home.html")+js+ " " + plot1 + plot2+ plot3
    print('This function was executed')
    if request.method == 'POST':
        print('This condition was executed')
        city = request.form['city']
        job_type = request.form['Job Type']
        print(city, job_type)
        return render_template('layout.html')

        # os.system('python code/data_analysis.py')

        # return js+ " " + plot1 + plot2+ plot3

# Running the app

if __name__ == "__main__":
    app.debug = True
    app.run()