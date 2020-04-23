import requests
from requests_oauthlib import OAuth1



requests.get("<a href='https://www.glassdoor.com/index.htm'>powered by <img src='https://www.glassdoor.com/static/img/api/glassdoor_logo_80.png' title='Job Search' /></a>")

response = requests.get("https://api.linkedin.com/v1/people/~")

x = response.json()

