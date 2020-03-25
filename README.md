## Simple Python Web Crawler

**Crawler Target:** http://www.zhaihehe.com/?/authentication_anchor/0

**Crawler Target:** https://kolranking.com/

**Crawler Target:** https://read.douban.com/category?kind=1

### Prerequisites

**PhantomJS:** this allow WebDriver to fetch ajax data in the website

- `sudo apt-get install phantomjs`

- change `executable_path` to your phantomjs local path, `/usr/bin/phantomjs`

- `pytesseract` require `tesseract-ocr` -> `sudo apt-get install tesseract-ocr`

- `chromedriver` http://chromedriver.storage.googleapis.com/index.html

### Basic Installation

- `git clone git@github.com:chandchen/net-pandas.git`

- `cd net-pandas`

- `mkvirtualenv -a . net-pandas -p python3.6`

- `pip install -r requirements.txt`

## Using Web Crawler

- `python web_robots.py`

- Type in username and password, and Go!
