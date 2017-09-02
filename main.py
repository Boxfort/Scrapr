#import libraries
import urllib2
import urllib
import threading
import sys
import argparse
import re, urlparse
import os
from bs4 import BeautifulSoup

soup = BeautifulSoup

#Defining command line arguments
parser = argparse.ArgumentParser(description='Download images from a tumblr.')
parser.add_argument('name', help='Name of blog')
parser.add_argument('-t', nargs=1, dest='tag', help='Download images with specified tag.')
parser.add_argument('-p', nargs=1, dest='page', type=int, default=[1], help='Page to start on.')
parser.add_argument('-n', nargs=1, dest='pages', type=int, default=[1], help='Number of pages to scrape.')
parser.add_argument('-d', nargs=1, dest='directory', type=int, default=[os.getcwd()], help='Directory to save the images.')

downloadCount = 0
directory = None

def getPageURLs(name, tag, page):

    #Build the blog url including any tags and page numbers
    url = 'http://'+str(name)+'.tumblr.com/'
    if tag != None:
        url += 'tagged/'+tag[0]+'/' 
    if page != None:
        url += 'page/'+str(page)

    print("Opening URL: " + url)

    try:
        page = urllib2.urlopen(url)
    except Exception:
        return None

    #parse html
    html = soup(page, 'html.parser')
    posts = html.findAll('a')

    #Gather all of the post urls to get full size images
    urls = []
    for tag in posts:
        try:
            if "tumblr.com/post" in tag['href'] and tag['href'].startswith('http://'+str(name)+'.tumblr.com/'):
                urls.append(tag['href'])
        except Exception:
            pass
    return urls

def getImageURLs(urls):
    print("Retreiving Image URLs...")
    imgURLs = []
    for url in urls:
        
        try:
            page = urllib2.urlopen(iriToUri(url))
            html = soup(page, 'html.parser')
    
            allImages = html.findAll('img')

            for tag in allImages:
                try:
                    if "68.media" in tag['src'] and "/tumblr_static" not in tag['src'] and "avatar" not in tag['src'] and tag['src'] not in imgURLs:
                        imgURLs.append(tag['src'])
                        print(tag['src'])
                except Exception:
                    pass
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
    try:
        if not os.path.exists(directory):
            os.makedirs(os.path.join(directory))

        urllib.urlretrieve(url, os.path.join(directory, imgName))
        onDownloadComplete()
    except Exception as e:
        print(str(e))
        exit()

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
    global directory
    args = vars(parser.parse_args())
    directory = os.path.join(args['directory'][0], args['name'])

    for i in range(args['page'][0], args['page'][0] + args['pages'][0]):
        urls = getPageURLs(args['name'], args['tag'], i)
        if not urls:
            print("No images found.")
            exit()
        imgURLs = getImageURLs(urls)
        downloadImages(imgURLs)
    
if __name__ == "__main__": main()
