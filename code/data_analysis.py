# Name: Saani
# Date: 26th April 2020
# Title: TDI Capstone clean-data
# Purpose: Analyse data and create charts for website
# Inputs: 1. df_clean.csv
# Outputs: 1.
# Dependencies:
# 1. data_clean.py

import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import sys

# file_dir = os.path.dirname(__file__)
sys.path.append("/Users/saannidhyarawat/Desktop/Projects/TDI/TDI capstone/code/functions")
from job_title_bar_plot import job_title_bar_plot

# User specific title and city
# title = input("Enter Title Here")
# city = input("Enter City Here")
# title = "Data Scientist"
title = "Data"
city = "New York"


# Setting root and specifying directory
root = "/Users/saannidhyarawat/Desktop/Projects/TDI/TDI capstone"
os.chdir(root)

# Importing data
os.chdir(root+'/data')
df = pd.read_csv("df_clean.csv")

# Counting number of job applications by title and City
# city_bool = df['Company_city'].str.lower() == city.lower()
# title_bool = df['Job_Title'].str.lower() == title.lower()
city_bool = df['Company_city'].str.lower().str.contains(city.lower())
title_bool = df['Job_Title'].str.lower().str.contains(title.lower())

# Bar plot (conver into separate module)
# df_bar_plot1 = df.loc[(city_bool) & (title_bool), :][['id','Job_Title']].groupby('Job_Title').agg('count').reset_index().rename(columns={'id':'frequency'})
df_bar_plot1 = df.loc[(city_bool) & (title_bool), :][['Company_city','Job_Title']].groupby('Job_Title').agg('count').reset_index().rename(columns={'Company_city':'frequency'})
data_bar = [go.Bar(x=df_bar_plot1['Job_Title'], y=df_bar_plot1['frequency'], width=0.5)]
layout = go.Layout(title = f'Number of Related Job Postings in {city}', xaxis_tickangle = -90)
fig = go.Figure(data=data_bar, layout=layout)
fig.layout.template = 'plotly_white'
pyo.plot(fig)

## Out of the 9 companies with highest n.o of job postings, which company is offering the highest salary on average
# plot4 = df_sal_no_dup.loc[df_sal_no_dup['Company'].isin(plot3['Company'].unique()), :]
# plot4 = plot4[['Company','Annual_Max_Salary']].groupby('Company').agg('mean').reset_index().rename(columns = {'Annual_Max_Salary' : 'Average Salary'})
# data_bar2 = [go.Bar(x = plot4['Company'], y = plot4['Average Salary'], name = 'company_mean_sal_barplot', marker = dict(color = '#FF7F0E'), width = 0.5)]
# layout = go.Layout(title = 'Average Salary offered by Companies with 10 or more Data Science job postings', xaxis_tickangle = -90)
# fig = go.Figure(data = data_bar2, layout = layout)
# fig.layout.template = 'plotly_white'
# pyo.plot(fig)

# pie chart
# proportion of major cities' market
df_pie = df.copy()
df_pie.loc[df_pie['Company_city'] == city, 'city'] = city
df_pie.loc[~(df_pie['Company_city'] == city), 'city'] = "Other"
df_pie = df_pie[['Company_city', 'city']].groupby('city').agg('count').reset_index().rename(columns={'Company_city':'count'})
df_pie.loc[:, 'proportion'] = df_pie['count']/df_pie['count'].sum()
data_pie = [go.Pie(labels=df_pie['city'], values=df_pie['proportion'])]
layout = go.Layout(title = f'{city} Metropolitan Market Share')
fig = go.Figure(data=data_pie, layout=layout)
pyo.plot(fig)

# Top 10 salaries offered in the city
df_bar_plot2 = df.loc[(city_bool) & (title_bool), :].sort_values('Annual_Salary', ascending=False).iloc[:10,:]
data_bar = [go.Bar(x=df_bar_plot2['Company'], y=df_bar_plot2['Annual_Salary'], marker = dict(color = '#FF7F0E'), width = 0.5)]
layout = go.Layout(title = f'Top 10 Companies Offering Highest Salaries in {city}', xaxis_tickangle = -90)
fig = go.Figure(data=data_bar, layout=layout)
fig.layout.template = 'plotly_white'
pyo.plot(fig)




