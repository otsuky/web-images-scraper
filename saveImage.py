import os
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://news.yahoo.co.jp/list/"
download_dir = "data"
sleep_time_sec = 100 / 1000


req = urllib.request.Request(url)
html = urllib.request.urlopen(req)

soup = BeautifulSoup(html, "html.parser")

src_list = [img.get("src") for img in soup.find_all("img")]


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(
            dst_path, "wb"
        ) as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


def download_file_to_dir(url, dst_dir):
    download_file(url, os.path.join(dst_dir, os.path.basename(url)))


def download_images_from_src_list(src_list, dst_dir):
    for url in src_list:
        file_path = urljoin(url, urlparse(url).path)
        print(file_path)
        # download_file_to_dir(file_path, dst_dir)
        time.sleep(sleep_time_sec)


download_images_from_src_list(src_list, download_dir)
