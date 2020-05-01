# WhatIsMyBrowser.com Scraper

Anti-detection Python Scraper for WhatIsMyBrowser.com

## Problem

WhatIsMyBrowser.com blocks IPs if the script uses `Requests` and `BeautifulSoup4`.

## Resolution

Instead, the script takes advantage of Selenium Firefox web driver in headless mode and scrape WhatIsMyBrowser.com without the IP being blocked.

## NOTE

For the comparison purposes, this script has kept the method using `Requests` and `BeautifulSoup4` by simply passing an argument `method='requests'`. Before trying this option, it is highly recommended to switch a throw-away IP.

```python
# Make the changes in main.py accordingly.
if __name__ == "__main__":
    for row in what_is_my_browser(method='requests'):
        print(row)
```

## How-to

(Debian or Debian-based OS)  
Open the terminal, and run the command below.

Clone this project.

```shell
git clone https://github.com/0xboz/whatismybrowser_com_scraper.git
cd whatismybrowser_com_scraper
```

Create an virtual environment for this project.

```shell
python3 -m venv venv
```

Activate venv and install all required packages.

```shell
source venv/bin/activate
(venv) pip install -r requirements.txt
```

Run the script.

```shell
(venv) python main.py
```
