# Copyright 2018, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


from clint.textui import progress
import logging
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# TODO: hide this somewhere in the database, options
ilias_url = "https://ilias.uni-freiburg.de"
login_url = ilias_url + "/shib_login.php"

usrname_id = 'LoginForm_username'
pw_id = 'LoginForm_password'
submit_name = 'yt0'
title_substring = 'ILIAS'


class browser_handler:
    def __init__(self, runner, logger=None, headless=False):
        self.runner = runner
        self.logger = logging.getLogger(logger.name + '.browser_handler')
        self.browser_options = Options()

        try:
            logger.info("Trying to import CEF.")
            from cefpython3 import cefpython as cef
            self.driver = webdriver.Chrome
            path = "todo"
        except ImportError:
            logger.info("Failed. Falling back to external firefox.")
            self.driver = webdriver.Firefox
            self.browser_options.headless = headless

    def create_driver(self):
        self.driver = self.driver(options=self.browser_options)

    def login(self, username, password):
        self.logger.info("Logging in at {}".format(login_url))

        self.driver.get(login_url)

        # Fill the login form and submit it
        self.driver.find_element_by_id(usrname_id).send_keys(username)
        self.driver.find_element_by_id(pw_id).send_keys(password)
        self.driver.find_element_by_name(submit_name).submit()

        # wait for succesful login and redirect
        WebDriverWait(self.driver, 30).until(EC.title_contains(title_substring))

        # for page_url in page_urls:
        #     # find video file in webpage
        #     driver.get(page_url)
        #     el = driver.find_element_by_xpath("//source[@type='video/mp4']")
        #     video_url = el.get_attribute('src')
        #
        #     print("Extracted video URL {}".format(video_url))
        #     video_url = video_url.split('.mp4')[0] + '.mp4'
        #
        #     driver.get(video_url)
        #     video_title = driver.title
        #     file_name = video_title
        #
        #     cookies = driver.get_cookies()
        #
        #     session = requests.Session()
        #     for cookie in cookies:
        #         session.cookies.set(cookie['name'], cookie['value'])
        #
        #     print("Requesting video.")
        #     video = session.get(video_url, stream=True)  # , headers=headers)
        #     print("ILIAS answering with response code {}.".format(
        #         video.status_code))
        #     print("Starting download to file {}".format(file_name))
        #
        #     with open(file_name, 'wb') as f:
        #         total_length = int(video.headers.get('content-length'))
        #         for chunk in progress.bar(video.iter_content(chunk_size=1024),
        #                                   expected_size=(total_length/1024) + 1):
        #             if chunk:
        #                 f.write(chunk)
        #                 f.flush()
        #
        # driver.quit()
