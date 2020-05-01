import os

# root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# bin directory
BIN_DIR = os.path.join(ROOT_DIR, 'bin')

# selenium web driver
SELENIUM_DIR = os.path.join(BIN_DIR, 'selenium')
GECKO_DRIVER = os.path.join(SELENIUM_DIR, 'geckodriver-v0.26.0-linux64/geckodriver')
SERVICE_LOG_PATH = '/dev/null'

# URLs
WHAT_IS_MY_BROWSER = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'