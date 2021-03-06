#import libraries
import urllib2
import urllib
import threading
import sys
import argparse
import re
import urlparse
import os
from bs4 import BeautifulSoup

soup = BeautifulSoup

#Defining command line arguments
parser = argparse.ArgumentParser(description='download images from a tumblr.')
parser.add_argument('name', help='name of blog')
parser.add_argument('-t', nargs=1, dest='tag', help='download images with specified tag.')
parser.add_argument('-p', nargs=1, dest='page', type=int, default=[1], help='page to start on.')
parser.add_argument('-n', nargs=1, dest='pages', type=int, default=[1], help='number of pages to scrape.')
parser.add_argument('-d', nargs=1, dest='directory', default=[os.getcwd()], help='directory to save the images.')

totalDownload = 0
downloadCount = 0
directory = None

def get_page_urls(name, tag, page):

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

def get_image_urls(urls):
    print("Retreiving Image URLs...")
    global totalDownload
    global downloadCount
    downloadCount = 0
    totalDownload = 0
    imgURLs = []
    for url in urls:
        
        try:
            page = urllib2.urlopen(iri_to_uri(url))
            html = soup(page, 'html.parser')
    
            allImages = html.findAll('img')

            for tag in allImages:
                try:
                    if "68.media" in tag['src'] and "/tumblr_static" not in tag['src'] and "avatar" not in tag['src'] and tag['src'] not in imgURLs:
                        imgURLs.append(tag['src'])
                        totalDownload += 1
                        print(tag['src'])
                except Exception:
                    pass
        except Exception:
            pass

    return imgURLs

def download_images(imgURLs):
    #Create a thread for each image to download concurrently
    threads = [threading.Thread(target=download_image, args=(url,)) for url in imgURLs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("\nDownloads Complete.")

def download_image(url):
    imgName = url.rsplit('/', 1)[1]
    try:
        if not os.path.exists(directory):
            os.makedirs(os.path.join(directory))

        urllib.urlretrieve(url, os.path.join(directory, imgName))
        on_download_complete(imgName)
    except Exception as e:
        print(str(e))
        exit()

def on_download_complete(imgName):
    length = 60
    global downloadCount
    downloadCount += 1
    filled = int(round(length * downloadCount / float(totalDownload)))
    percents = round(100.0 * downloadCount / float(totalDownload), 1)
    bar = '=' * filled + '-' * (length - filled)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', imgName))
    sys.stdout.flush()

def url_encode_non_ascii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iri_to_uri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else url_encode_non_ascii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )
   
def main():
    global directory
    args = vars(parser.parse_args())
    directory = os.path.join(args['directory'][0], args['name'])

    #Download images from starting page to range specified
    for i in range(args['page'][0], args['page'][0] + args['pages'][0]):
        urls = get_page_urls(args['name'], args['tag'], i)
        if not urls:
            print("No images found.")
            exit()
        imgURLs = get_image_urls(urls)
        download_images(imgURLs)
    
if __name__ == "__main__": main()
