import os
import threading
import time

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


app = Flask(__name__)


@app.route('/visit/<uid>')
def visit(uid):
    thread = threading.Thread(target=bot, args=(uid,))
    thread.start()
    return 'OK'


def bot(uid):
    ###### Begin of code that is not a part of the challenges ######
    chrome_options = Options()

    prefs = {
        "download.prompt_for_download": True,
        "download.default_directory": "/dev/null"
    }

    chrome_options.add_experimental_option(
        "prefs", prefs
    )
    chrome_options.add_argument('headless')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('disable-background-networking')
    chrome_options.add_argument('disable-default-apps')
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('disable-sync')
    chrome_options.add_argument('disable-translate')
    chrome_options.add_argument('hide-scrollbars')
    chrome_options.add_argument('metrics-recording-only')
    chrome_options.add_argument('no-first-run')
    chrome_options.add_argument('safebrowsing-disable-auto-update')
    chrome_options.add_argument('media-cache-size=1')
    chrome_options.add_argument('disk-cache-size=1')
    chrome_options.add_argument('disable-setuid-sandbox')
    chrome_options.add_argument('--js-flags=--noexpose_wasm,--jitless')

    # service = Service(executable_path='/bot/chromedriver')
    # client = webdriver.Chrome(options=chrome_options, service=service)
    client = webdriver.Chrome(options=chrome_options)
    ###### End of code that is not a part of the challenges ######

    time.sleep(3)
    client.get(f"http://127.0.0.1:1337/")
    time.sleep(3)
    client.add_cookie({'name': 'FLAG', 'value': os.getenv('FLAG', 'VCS{FLAG}')})
    client.get(f"http://127.0.0.1:1337/profile/{uid}")
    time.sleep(60)

    client.quit()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082, debug=True)
