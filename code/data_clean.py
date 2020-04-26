# Name: Saani
# Date: 25th April 2020
# Title: TDI Capstone clean-data
# Purpose: Clean scraped data
# Inputs: 1. df_data_science_jobs.csv
# Outputs: 1.
# Dependencies:
# 1.

# Importing libraries
import os
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# Loading directory and establishing root
root = "/Users/saannidhyarawat/Desktop/Projects/TDI/TDI capstone"

os.chdir(root+'/data')

# df = pd.read_csv('df_all_jobs.csv')
df = pd.read_csv('df_data_science_jobs.csv')

# len(df)
# df.head()

# Renaming columns
cols = {'Unnamed: 0':'id', '0': 'Job_Title', '1':'Company', '2': 'Company_Address', '3': 'Salary','4': 'Job_Summary'}
df = df.rename(columns=cols)
# Total rows = 8,267

# Removing rows with missing salary information
sal_boolean = df['Salary'].isna()
df_sal = df.loc[~sal_boolean, :]
print(len(df) - len(df_sal))
# Removed rows = 7,019
# Remaining rows with Salary info: 1,248

# Removing rows with no company address
address_boolean = df['Company_Address'].isna()
df_comp_address = df_sal.loc[~address_boolean, :]
print(len(df_sal) - len(df_comp_address))
# Removed rows = 0

# Clearing all rows which contain duplicate
df_2 = df_comp_address.loc[~(df_comp_address[['Job_Title', 'Company', 'Company_Address', 'Salary', 'Job_Summary']].duplicated()), :]
print(len(df_2))
print(len(df_comp_address) - len(df_2))
# Removed rows = 0

# Cleaning salary column

# Some observation contain '++' in the variable, removing these '++' symbols
# df_2.loc[df_2['Sal_duration'] == '++', :]
df_2['Salary'] = df_2['Salary'].apply(lambda x: str(x).replace('++',''))

# Getting rid of extra space around the strings
for i in list(cols.values())[1:]:
    df_2[i] = df_2[i].apply(lambda x: str(x).strip())

# Storing different salary types
df_2['Sal_type'] = df_2['Salary'].apply(lambda x: str(x).split(' ')[-1])

sal_types = ['year', 'hour', 'month', 'week', 'day']

df_2 = df_2.loc[df_2['Sal_type'].isin(sal_types), :]

# Storing salary cap (max salary for ranges)
# x = df_2.copy()
df_2['Sal_cap'] = df_2['Salary'].apply(lambda x: str(x).split(' ')[-3].replace('$','').replace(',','').strip())

# Outliers
# One unique observation that pays per session. Because it is only one obs and I do not want to treat it differently. Solution: remove obs
# Also, One unique observation paying 'per flight hour'. removing this observation
# df_2 = df_2.loc[~((df_2['Sal_type'] == 'session') | (df_2['Sal_cap'] == 'per')), :].reset_index(drop=True)
# len(df_2)

# giving salary caps appropriate treatment (based on sal type or duration) (Converting into annual salary)
# Converting all monthly, hourly, and weekly salaries into yearly
## Yearly
yr_bool = df_2['Sal_type'] == 'year'
df_2.loc[(yr_bool), 'Annual_Salary'] = df_2.loc[yr_bool, 'Sal_cap'].apply(lambda x: float(x))
## Monthly
mon_bool = df_2['Sal_type'] == 'month'
df_2.loc[(mon_bool), 'Annual_Salary'] = df_2.loc[mon_bool,'Sal_cap'].apply(lambda x: float(x) * 12) # working 12 months a year
## Hourly (assuming 40 work hours and 52 weeks)
hour_bool = df_2['Sal_type'] == 'hour'
df_2.loc[(hour_bool), 'Annual_Salary'] = df_2.loc[hour_bool,'Sal_cap'].apply(lambda x: float(x) * 40 * 52) # working 40 hours a week, for 52 weeks
## Weekly
week_bool = df_2['Sal_type'] == 'week'
df_2.loc[(week_bool), 'Annual_Salary'] = df_2.loc[week_bool, 'Sal_cap'].apply(lambda x: float(x) * 52) # Working 52 weeks
## Hourly
day_bool = df_2['Sal_type'] == 'day'
df_2.loc[(day_bool), 'Annual_Salary'] = df_2.loc[day_bool, 'Sal_cap'].apply(lambda x: float(x) * 5 * 52) # Working 5 days a week, for 52 weeks


# df_2_srtd = df_2.sort_values(by='Annual_Salary', ascending=False)
# max(df_2['Annual_Salary'])
# min(df_2['Annual_Salary'])
del(df_2['Sal_type'])
del(df_2['Sal_cap'])
del(df_2['Salary'])


# To-do:
# 1. deal with duplicate observations
# 2. Clean Company address column
# 3. Text mining: Job Summary

# Cleaning address column
address_boolean = df_2['Company_Address'].str.contains(',')
df_2.loc[~(address_boolean), 'Company_State'] = df_2.loc[~(address_boolean), 'Company_Address'].apply(lambda x: str(x))
df_2.loc[(address_boolean), 'Company_State'] = df_2.loc[(address_boolean), 'Company_Address'].apply(lambda x: str(x).split(',')[1].strip().split(' ')[0])


df_2['Company_city'] = df_2.loc[:, 'Company_Address'].apply(lambda x: str(x).split(',')[0].strip())

df_2.reset_index(drop = True)

# Output

df_2.to_csv("df_clean.csv", index=False)
os.chdir(root)
os.getcwd()
