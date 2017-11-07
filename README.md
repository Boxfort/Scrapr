# Scrapr
Scrapr is a simple command line image scraper for https://www.tumblr.com.

## Requirements
* Python 2.7
* BeautifulSoup
  * `pip install beautifulsoup4`
* Python-dev
  * `sudo apt-get install python-dev`

## Usage
**python main.py [-h] [-t TAG] [-p PAGE] [-n PAGES] [-d DIRECTORY] name**

Positional arguments:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name of blog

Optional arguments:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-h, --help&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show this help message and exit
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-t TAG&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;download images with specified tag.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-p PAGE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;page to start on.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-n PAGES&nbsp;&nbsp;&nbsp;&nbsp;number of pages to scrape.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-d DIRECTORY &nbsp;&nbsp;  directory to save the images.

