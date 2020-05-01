from settings import GECKO_DRIVER, WHAT_IS_MY_BROWSER, SERVICE_LOG_PATH

from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import logging
import re
from urllib.parse import urljoin

def isnumeric(value):
    """
    Determine if the string is numeric.
    :param value: string
    :return: Boolean
    """
    if value.isdigit():
        return True
    else:
        try:
            float(value)
            return True
        except ValueError:
            return False

def what_is_my_browser(**kwargs):
    """
    WhatIsMyBrowser.com User Agents table row generator.
    Risk: IP might be blocked if scraping occurs too frequently with Requests & BeautifulSoup.
    Therefore, this function defaults to scraping with Selenium.

    Scrape browser user agents from
    https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/

    :Return:
        A Generator. 
    """
    method = kwargs.get('method').lower() if kwargs.get('method') else None

    if method and 'requests' in method:
        r = requests.get(url=WHAT_IS_MY_BROWSER)
        all_urls = []
        if r.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            last_page_text = soup.find(string=re.compile(r'^(Last Page)'))
            last_page_number = int(''.join([e for e in last_page_text if e.isdigit()]))
            for index, _ in enumerate(range(0, last_page_number), start=1):
                all_urls.append(urljoin(WHAT_IS_MY_BROWSER, str(index)))

        for url in all_urls:
            r = requests.get(url=url)
            if r.ok:
                soup = BeautifulSoup(r.text, 'html.parser')
                for row in soup.find_all(name='tr')[1:]:
                    columns = row.find_all('td')
                    column_keys = ['user_agent', 'software', 'os', 'layout_engine', 'popularity']
                    column_values = [column.get_text() for column in columns]
                    column_dict = dict(zip(column_keys, column_values))

                    # Parse software version
                    column_dict['software_version'] = float(column_dict['software'].split()[-1]) if isnumeric(
                        column_dict['software'].split()[-1]) else 0.0

                    yield {
                        'user_agent': column_dict['user_agent'],
                        'software': column_dict['software'],
                        'software_version': column_dict['software_version'],
                        'os': column_dict['os'],
                        'layout_engine': column_dict['layout_engine'],
                        'popularity': column_dict['popularity']
                    }
            else:
                logging.error('IP blocked')

    else:  # Defaults to the method using Selenium library
        
        firefox_options = Options()
        firefox_options.headless = True  # Headless mode

        driver = Firefox(executable_path=GECKO_DRIVER, options=firefox_options, service_log_path=SERVICE_LOG_PATH)
        driver.get(WHAT_IS_MY_BROWSER)
        wait_10 = WebDriverWait(driver, 10)
        while True:
            rows = wait_10.until(ec.presence_of_all_elements_located((By.XPATH, '//tr')))
            for row in rows[1:]:
                columns = row.find_elements_by_xpath('.//td')
                column_keys = ['user_agent', 'software', 'os', 'layout_engine', 'popularity']
                column_values = [column.text for column in columns]
                column_dict = dict(zip(column_keys, column_values))

                # Parse software version
                column_dict['software_version'] = float(column_dict['software'].split()[-1]) if isnumeric(
                    column_dict['software'].split()[-1]) else 0.0

                yield {
                    'user_agent': column_dict['user_agent'],
                    'software': column_dict['software'],
                    'software_version': column_dict['software_version'],
                    'os': column_dict['os'],
                    'layout_engine': column_dict['layout_engine'],
                    'popularity': column_dict['popularity']
                }

            try:
                next_btn = wait_10.until(ec.element_to_be_clickable(
                    (By.XPATH, '//a[contains(text(), ">")]')))
                next_btn.click()
            except TimeoutException:
                driver.quit()
                break  # Exit while loop if next button is disabled.


if __name__ == "__main__":
    for row in what_is_my_browser():
        print(row)
