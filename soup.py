#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests,sys,csv,json

logs = open("logs/logs.txt", "w")
logs.seek(0)
logs.truncate()
url="http://ufm.edu/Portal"
# Make a GET request to fetch the raw HTML content
try:
    html_content = requests.get(url).text
except:
    print(f"unable to get {url}")
    sys.exit(1)

# Parse the html content, this is the Magic ;)
soup = BeautifulSoup(html_content, "lxml")

# print if needed, gets too noisy
#print(soup.prettify())

print("Diego Quan \n============================= \n1. Portal \n")

print("{} \n".format(soup.title.string))

print("{} \n".format(soup.find('a', href="#myModal").get_text()))

print("{}".format(soup.find('a', href="tel:+50223387700").get_text()))

for x in soup.find_all('div', class_='menu-key'): 
    print("\n", x.get_text(strip=True))

if len(soup.find_all(href=True)) <= 30:
    for x in soup.find_all(href=True): 
        print("\n", x['href'])
else:
    print("\nOutput exceeds 30 lines, it can be found on logs/logs.txt")
    for x in soup.find_all(href=True):
        if x['href'] == '#':
            pass
        else:
            logs.write("\n {}".format(x['href']))

print("\n{}".format(soup.find(id="ufmail_")['href']))

print("\n{}".format(soup.find(id="miu_")['href']))
