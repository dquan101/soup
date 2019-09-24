#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests,sys,csv,json,re

logs = open("logs/logs.txt", "w+")
logs.seek(0)
logs.truncate()
url="http://ufm.edu"
url_portal = url + "/Portal"
# Make a GET request to fetch the raw HTML content
try:
    html_content = requests.get(url_portal).text
except:
    print(f"unable to get {url}")
    sys.exit(1)

# Parse the html content, this is the Magic ;)
soup = BeautifulSoup(html_content, 'html.parser')

# print if needed, gets too noisy
#print(soup.prettify())
def Portal():
    print("Diego Quan \n============================= \n1. Portal \n")

    print("{} \n".format(soup.title.string))

    print("{} \n".format(soup.find('a', href="#myModal").get_text()))

    print("{}".format(soup.find('a', href="tel:+50223387700").get_text()))

    for x in soup.find_all('div', class_='menu-key'): 
        print("\n{}".format(x.get_text(strip=True)))

    if len(soup.find_all(href=True)) <= 30:
        for x in soup.find_all(href=True): 
            print("\n{}".format(x['href']))
    else:
        print("\nOutput exceeds 30 lines, it can be found on logs/logs.txt")
        for x in soup.find_all(href=True):
            if x['href'] == '#':
                pass
            else:
                logs.write("\n {}".format(x['href']))

    print("\n{}".format(soup.find(id="ufmail_")['href']))

    print("\n{}".format(soup.find(id="miu_")['href']))

    for y in soup.find_all('img'):
        print('\n{}'.format(y['src']))
    a = soup.find_all('a')
    print("\nThere's a total of {} <a>".format(len(a)))

    with open('as.csv', 'w+') as writeFile:
        writer = csv.writer(writeFile)
        for z in a:
            row = [z.get_text(), z['href']]
            writer.writerow(row)


    logs.close()
def Estudios(soup):
    print("\n============================= \n2. Estudios \n")

    url_estudios = url + soup.find(href="/Estudios")['href']
    html_content = requests.get(url_estudios).text
    soup = BeautifulSoup(html_content, 'html.parser')
    for string in soup.find(id="topmenu").stripped_strings:
        print(string)
    print("\n")
    for x in soup.find_all('div', class_='estudios'):
        print(x.get_text())
    print("\n")
    for x in soup.find(class_='leftbar').find_all('li'):
        print(x.get_text())
    print("\n")
    for x in soup.find(class_='social pull-right').find_all('a'):
        print(x.get('href'))

    a = soup.find_all('a')
    print("\nThere's a total of {} <a>".format(len(a)))


def Carrera(soup):

    url_cs = "https://fce.ufm.edu/carrera/cs/"
    html_content = requests.get(url_cs).text
    soup = BeautifulSoup(html_content, 'html.parser')

    print("\n============================= \n3. CS \n")
    print("{} \n".format(soup.title.string))

    logo = soup.find(href='https://fce.ufm.edu').find('img').get('src')
    image = requests.get(logo, allow_redirects=True)
    open('logo_ufm.png', 'wb').write(image.content)

    print("\n{}".format(soup.find('meta', property='og:type')))
    print("\n{}".format(soup.find('meta', property='og:title')))

    a = soup.find_all('a')
    print("\nThere's a total of {} <a>".format(len(a)))

    div = soup.find_all('div')
    print("\nThere's a total of {} <div>".format(len(div)))


def Directorio():
    print("\n============================= \n4. Directorio \n")

    url_directorio = url + "/Directorio"
    html_content = requests.get(url_directorio).text
    soup = BeautifulSoup(html_content, 'html.parser')
    mails = []
    for x in soup.find(id="mw-content-text").find_all("a", href=re.compile("mailto")):
        mails.append(x.get('href'))
    mails.sort()

    with open('logs/4directorio_emails.txt', 'w+') as emails:
        for item in mails:
            emails.write('%s\n' % item)
    emails.close()

    vocales = 0
    for item in mails:
        if item[7] in ('a','e','i','o','u'):
            vocales += 1
    print("La cantidad de correos que inician con vocal son: {}".format(vocales))

    direcciones = {}
    pairs = []
    for x in soup.find_all('tr'):
        if len(x.contents) == 10:
            pares = []
            p = x.contents[9].get_text().strip().split(',')[0]
            q = x.contents[1].get_text().strip()
            pares.append(p)
            pares.append(q)
            pairs.append(pares)

    for x in pairs:
        direcciones[x[0]] = []
    for x in pairs:
        for key in direcciones.items():
            if key == x[0]:
                direcciones[key].append(x[1])
    print("\nLas direcciones fueron impresas en el archivo 4directorio_address.json")
    with open('logs/4directorio_address.json', 'w+') as f:
            json.dump(direcciones, f)

    
try:    
    if sys.argv[1] == '1':
        Portal()
    if sys.argv[1] == '2':
        Estudios(soup)
    if sys.argv[1] == '3':
        Carrera(soup)
    if sys.argv[1] == '4':
        Directorio()
except IndexError:
    Portal()
    Estudios(soup)
    Carrera(soup)
    Directorio()