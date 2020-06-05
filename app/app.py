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

# import code.data_analysis.data_import


app = Flask(__name__)

@app.route('/')
def show():
    # return "Hello, world."
    return render_template("home.html")
    # return f"Method used: {request.method}"

# @app.route('/submit', methods = ["GET", "POST"])
@app.route('/submit', methods = ["GET", "POST"])
def submit():

    if request.method == 'POST':
        # return f"Method used: {request.method}"
        # return f"job type: {request.form['Job Type']} and city: {request.form['city']}"
        city = request.form['city']
        job_type = request.form['Job Type']
        # os.system('python ../code/data_analysis.py')

        title = job_type
        city = city

        # Setting root and specifying directory

        # Importing data
        df = pd.read_csv("df_clean.csv")

        # Counting number of job applications by title and City
        title_split = title.lower().replace(" ","|")
        city_bool = df['Company_city'].str.lower().str.contains(city.lower())
        title_bool = df['Job_Title'].str.lower().str.contains(title_split)

        js = f'<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'

        # Bar plot (convert into separate module)
        df_bar_plot1 = df.loc[(city_bool) & (title_bool), :][['Company_city', 'Job_Title']].groupby('Job_Title').agg(
            'count').reset_index().rename(columns={'Company_city': 'frequency'})
        data_bar = [go.Bar(x=df_bar_plot1['Job_Title'], y=df_bar_plot1['frequency'], width=0.5)]
        layout = go.Layout(title=f'Number of Related Job Postings in {city}: Trending Job Posting titles can be observed from this graph', xaxis_tickangle=-20)
        fig = go.Figure(data=data_bar, layout=layout)
        fig.layout.template = 'plotly_white'
        plot1 = pyo.plot(fig, include_plotlyjs=False, output_type='div')

        # pie chart
        # proportion of major cities' market
        df_pie = df.copy()
        df_pie.loc[df_pie['Company_city'] == city, 'city'] = city
        df_pie.loc[~(df_pie['Company_city'] == city), 'city'] = "Other"
        df_pie = df_pie[['Company_city', 'city']].groupby('city').agg('count').reset_index().rename(
            columns={'Company_city': 'count'})
        df_pie.loc[:, 'proportion'] = df_pie['count'] / df_pie['count'].sum()
        data_pie = [go.Pie(labels=df_pie['city'], values=df_pie['proportion'])]
        layout = go.Layout(title=f'{city} Metropolitan Market Share')
        fig = go.Figure(data=data_pie, layout=layout)
        fig.update_layout(
            autosize=False,
            width=500,
            height=500,
            # margin=dict(l=100, r=100, b=300, t=300, pad=4))
            margin=dict(l=20, r=20, t=30, b=30))
        plot2 = pyo.plot(fig, include_plotlyjs=False, output_type='div')

        # Top 10 salaries offered in the city
        df_bar_plot2 = df.loc[(city_bool) & (title_bool), :].sort_values('Annual_Salary', ascending=False).iloc[:10, :]
        data_bar = [
            go.Bar(x=df_bar_plot2['Company'], y=df_bar_plot2['Annual_Salary'], marker=dict(color='#FF7F0E'), width=0.5)]
        layout = go.Layout(title=f'Top 10 Job Postings Offering Highest Salaries in {city}: Top players in the market based on Salary', xaxis_tickangle=-90)
        fig = go.Figure(data=data_bar, layout=layout)
        fig.layout.template = 'plotly_white'
        plot3 = pyo.plot(fig, include_plotlyjs=False, output_type='div')

        return js + plot1 + plot2 + plot3

# Running the app

if __name__ == "__main__":
    app.debug = False
    app.run()
