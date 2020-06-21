# Copyright 2018, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


from clint.textui import progress
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class browser_handler:
    def download(page_urls, cookies=None):

        for page_url in page_urls:
            # find video file in webpage
            driver.get(page_url)
            el = driver.find_element_by_xpath("//source[@type='video/mp4']")
            video_url = el.get_attribute('src')

            print("Extracted video URL {}".format(video_url))
            video_url = video_url.split('.mp4')[0] + '.mp4'

            driver.get(video_url)
            video_title = driver.title
            file_name = video_title

            cookies = driver.get_cookies()

            session = requests.Session()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            print("Requesting video.")
            video = session.get(video_url, stream=True)  # , headers=headers)
            print("ILIAS answering with response code {}.".format(
                video.status_code))
            print("Starting download to file {}".format(file_name))

            with open(file_name, 'wb') as f:
                total_length = int(video.headers.get('content-length'))
                for chunk in progress.bar(video.iter_content(chunk_size=1024),
                                          expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()

        driver.quit()
