import urllib.request as ur

url = 'http://www.google.com'
conn = ur.urlopen(url)

print(conn)

data = conn.read()

print(conn.status)
print(conn.getheader('Content-Type'))

for key, value in conn.getheaders():
    print(key, value)

print(data)

# Requests API
import requests

url = 'http://www.google.com'
resp = requests.get(url)
print(resp)
print(resp.text)

import webbrowser
url = 'http://www.python.org/'
webbrowser.open(url)
webbrowser.open_new(url)

# Web scraping
def get_links(url):
    import requests
    from bs4 import BeautifulSoup as soup

    result = requests.get(url)
    page = result.text
    doc = soup(page)
    links = [element.get('href') for element in doc.find_all('a')]
    return links

import sys

url = 'http://www.nytimes.com'

print('Links in', url)
for link in get_links(url):
    print(link)
