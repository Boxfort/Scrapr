#import libraries
import urllib2
import urllib
import threading
import sys
import argparse
import re, urlparse
from bs4 import BeautifulSoup

soup = BeautifulSoup

parser = argparse.ArgumentParser(description='Download images from images from a tumblr.')
parser.add_argument('name', help='The name of the tumblr.')
parser.add_argument('--tags', nargs='*', dest='tags', help='Image must contain one or more of the supplied tags.')

downloadCount = 0
args = []

def getPageURLs():
    url = 'http://'+str(args['name'])+'.tumblr.com/'
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
        page = urllib2.urlopen(iriToUri(url))
        html = soup(page, 'html.parser')

        allImages = html.findAll('img')

        for tag in allImages:
            try:
                if "/tumblr_" in tag['src'] and "/tumblr_static" not in tag['src']:
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

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )
   
def main():
    global args
    args = vars(parser.parse_args())
    print(args)

    urls = getPageURLs()
    imgURLs = getImageURLs(urls)
    downloadImages(imgURLs)
    
if __name__ == "__main__": main()

