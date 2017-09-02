#import libraries
import urllib2
from bs4 import BeautifulSoup

soup = BeautifulSoup;

#test url
url = 'http://pacifist-stephania.tumblr.com/'
page = urllib2.urlopen(url)

#parse html
html = soup(page, 'html.parser')
posts = html.findAll('a')

for tag in posts:
    try:
        if tag.parent['class'][0] == 'post':
            print (tag['href'])
    except Exception:
        print("Parent has no class.")
