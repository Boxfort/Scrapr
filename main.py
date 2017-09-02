#import libraries
import urllib2
import urllib
import threading
import sys
from bs4 import BeautifulSoup

soup = BeautifulSoup
downloadCount = 0

def getPageURLs():
    #test url
    url = 'http://pacifist-stephania.tumblr.com/'
    print("Opening URL: " + url)
    page = urllib2.urlopen(url)

    #parse html
    html = soup(page, 'html.parser')
    posts = html.findAll('a')

    urls = []
    for tag in posts:
        try:
            if "tumblr.com/post" in tag['href']:
                urls.append(tag['href'])
        except Exception:
            pass
    return urls

def getImageURLs(urls):
    print("Retreiving Image URLs...")
    imgURLs = []
    for url in urls:
        page = urllib2.urlopen(url)
        html = soup(page, 'html.parser')

        allImages = html.findAll('img')

        for tag in allImages:
            try:
                if "/tumblr_" in tag['src']:
                    imgURLs.append(tag['src'])
            except Exception:
                pass
    return imgURLs

def downloadImages(imgURLs):
    threads = [threading.Thread(target=downloadImage, args=(url,)) for url in imgURLs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("\nDownloads Complete.")
        
def downloadImage(url):
    imgName = url.rsplit('/', 1)[1]
    urllib.urlretrieve(url, imgName)
    onDownloadComplete()

def onDownloadComplete():
    global downloadCount
    downloadCount = downloadCount + 1
    message = "\rImages Downloaded: " + str(downloadCount)
    sys.stdout.write(message)
    sys.stdout.flush()
   
def main():
    urls = getPageURLs()
    imgURLs = getImageURLs(urls)
    downloadImages(imgURLs)
    
if __name__ == "__main__": main()

