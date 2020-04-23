# Title: Indeed web data scraping
# Purpose: To extract data from Indeed's website using bs4 python module for TDI Capstone Project
# Created by: Saani Rawat
# Last modifed: 04/23/2020
# Data last scraped on: 04/23/2020, 2:00pm
# Output:
# 1.df_all_jobs.csv

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


###### FINAL SCRAPING  ##########

from datetime import datetime

start_time = datetime.now()

root = "/Users/saannidhyarawat/Desktop/Projects/TDI/TDI capstone"
os.chdir(root+"/code")

titles = ["data%20scientist", "quantitative%20analyst", "data%20analyst", "data%20engineer", "quant", "machine%20learning"]

cities = {"San+Francisco":"CA", "Charlotte":"NC", "New+York+City":"NY", "Boston":"MA", "Chicago":"IL", "Houston":"TX",
          "Los+Angeles":"CA", "Washington":"DC", "Phoenix":"AZ", "Philadelphia":"PA", "San+Antonio":"TX", "San+Diego":"CA",
          "Dallas":"TX", "San+Jose":"CA", "Seattle":"WA", "Atlanta":"GA"
          }

city_key = list(cities.keys())
city_val = list(cities.values())

jobs_info = []
for city, state in zip(city_key, city_val): # For each city in the dictionary
    for title in titles:
        # print(f'city: {city}, state: {state}')
        # for i in range(0, 10000, 10): # Open each page in the range
        # print(f'title: {title}')
        for i in range(20, 1000, 20):  # Open each page in the range

            # print("url: https://www.indeed.com/jobs?q=data%20scientist&l=" + city + "%2C+" + state + "&start=" + str(i))
            # print(f'page: {str(i)}')

            source = requests.get("https://www.indeed.com/jobs?q="+title+"&l=" + city + "%2C+" + state + "&start=" + str(i)) # Changes by every city

            # soup = BeautifulSoup(source, "html.parser")
            soup = BeautifulSoup(source.text, "lxml") # changes for every city

            for row in range(0, len(soup.select("div.jobsearch-SerpJobCard"))): # In each page, open each posting

                posting = soup.select("div.jobsearch-SerpJobCard")[row] # Changes by every city and

                # print(f'row num: {row}')

                # Title
                try:
                    title = posting.h2.a.text.strip()
                except Exception as e:
                    title = None

                try:
                    company_name = posting.find_all("span", class_="company")[0].text.strip()
                except Exception as e:
                    company_name = None

                # Company address
                try:  # Check if address exists
                    company_address = posting.select("div.location")[0].text.strip()
                except Exception as e:
                    try:
                        company_address = posting.select("span.location")[0].text.strip()
                    except Exception as e:
                        company_address = None  # Return None if it doesn't exist

                # Salary information
                try:  # Check if salary info exists
                    salary = posting.select("span.salaryText")[0].text.strip()
                except Exception as e:
                    salary = None  # Return None if it doesn't exist

                # Summary
                try:  # Check if job summary exists
                    job_summary = posting.select("div.summary")[0].text.strip()
                except Exception as e:
                    job_summary = None  # Return None if it doesn't exist

                if (title, company_name, company_address, salary, job_summary) not in jobs:
                    jobs_info.append((title, company_name, company_address, salary, job_summary))
                    # print(f'full job posting - title: {title}, company:{company_name}, salary: {salary}')


df_jobs = pd.DataFrame(jobs_info)
os.chdir(root+'/data')
df_jobs.to_csv("df_data_science_jobs.csv")
os.chdir(root)

end_time = datetime.now()
print(f'Time taken: {end_time - start_time}')
