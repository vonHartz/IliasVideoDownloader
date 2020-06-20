#!/usr/bin/python3

# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.

import click
from clint.textui import progress
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ilias_url = "https://ilias.uni-freiburg.de"
login_url = ilias_url + "/shib_login.php"


@click.command()
@click.argument('page_url', nargs=1, required=True)
@click.argument('rz_user', nargs=1, required=True)
@click.argument('password', nargs=1, required=True)
@click.argument('file_name', nargs=1, required=False)
def main(page_url, file_name, rz_user, password):
    """
    Logs into ILIAS and downloads the video specified by the given URL.

    Example:
        $ python download.py ilias-adress.de/this-video.mp4 my_video.mp4 xxx pw
    """

    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Firefox(options=browser_options)

    print("Logging in at {}".format(login_url))

    driver.get(login_url)

    # Fill the login form and submit it
    driver.find_element_by_id('LoginForm_username').send_keys(rz_user)
    driver.find_element_by_id('LoginForm_password').send_keys(password)
    driver.find_element_by_name("yt0").submit()

    # wait for succesful login and redirect
    WebDriverWait(driver, 30).until(EC.title_contains("ILIAS"))

    # find video file in webpage
    driver.get(page_url)
    el = driver.find_element_by_xpath("//source[@type='video/mp4']")
    video_url = el.get_attribute('src')

    print("Extracted video URL {}".format(video_url))
    video_url = video_url.split('.mp4')[0] + '.mp4'

    driver.get(video_url)
    video_title = driver.title
    file_name = file_name or video_title

    cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    print("Requesting video.")
    video = session.get(video_url, stream=True)  # , headers=headers)
    print("ILIAS answering with response code {}.".format(video.status_code))
    print("Starting download to file {}".format(file_name))

    with open(file_name, 'wb') as f:
        total_length = int(video.headers.get('content-length'))
        for chunk in progress.bar(video.iter_content(chunk_size=1024),
                                  expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


if __name__ == "__main__":
    main()
