#import libraries
import urllib2
import urllib
from bs4 import BeautifulSoup

soup = BeautifulSoup;

def getPageURLs():
    #test url
    url = 'http://pacifist-stephania.tumblr.com/'
    page = urllib2.urlopen(url)

    #parse html
    html = soup(page, 'html.parser')
    posts = html.findAll('a')

    urls = []
    for tag in posts:
        try:
            if tag.parent['class'][0] == 'post':
                urls.append(tag['href'])
        except Exception:
            pass
    return urls

def getImageURLs(urls):
    imgURLs = []
    for url in urls:
        page = urllib2.urlopen(url)
        html = soup(page, 'html.parser')

        allImages = html.findAll('img')

        for tag in allImages:
            try:
                if tag.parent.parent['class'][1] == 'photo':
                    imgURLs.append(tag['src'])
            except Exception:
                pass
    return imgURLs

def downloadImages(imgURLs):
    for imgURL in imgURLs:
        imgName = imgURL.rsplit('/', 1)[1];
        urllib.urlretrieve(imgURL, imgName)

def main():
    urls = getPageURLs()
    imgURLs = getImageURLs(urls)
    print(imgURLs)
    downloadImages(imgURLs)

if __name__ == "__main__": main()

