from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


###### FINAL SCRAPING  ##########

from datetime import datetime

root = "/Users/saannidhyarawat/Desktop/Projects/TDI/TDI capstone"
os.chdir(root+"/code")

start_time = datetime.now()

cities = {"San+Francisco":"CA", "Charlotte":"NC", "New+York+City":"CA", "Boston":"MA", "Chicago":"IL", "Houston":"TX",
          "Los+Angeles":"CA", "Washington":"DC", "Phoenix":"AZ", "Philadelphia":"PA", "San+Antonio":"TX", "San+Diego":"CA",
          "Dallas":"TX", "San+Jose":"CA", "Seattle":"WA", "Atlanta":"GA"
          }

city_key = list(cities.keys())
city_val = list(cities.values())

jobs_info = []
for city, state in zip(city_key, city_val): # For each city in the dictionary
    # for i in range(0, 10000, 10): # Open each page in the range
    for i in range(0, 10000, 10):  # Open each page in the range

        source = requests.get("https://www.indeed.com/jobs?q=data%20scientist&l=" + city + "%2C+" + state + "&start=" + str(i))

        # soup = BeautifulSoup(source, "html.parser")
        soup = BeautifulSoup(source.text, "lxml")

        for row in range(0, len(soup.select("div.jobsearch-SerpJobCard"))): # In each page, open each posting

            posting = soup.select("div.jobsearch-SerpJobCard")[row]

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

            jobs_info.append((title, company_name, company_address, salary, job_summary))

jobs_info_set = set(jobs_info)

df_all_jobs = pd.DataFrame(jobs_info_set)
os.chdir(root+'/data')
df_all_jobs.to_csv("df_data_science_jobs.csv")
os.chdir(root)

end_time = datetime.now()
print(f'Time taken: {end_time - start_time}')
