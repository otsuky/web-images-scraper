import os
import time
import pathlib
import urllib.error
import urllib.request


from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

sleep_time_sec = 100 / 1000


def download_file_to_dir(url, download_dir):
    download_path = pathlib.Path(download_dir + os.path.dirname(urlparse(url).path))
    download_path.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(url) as web_file, open(
            os.path.join(download_path, os.path.basename(url)), "wb"
        ) as local_file:
            local_file.write(web_file.read())
            print("✅ Saved")
    except urllib.error.URLError as e:
        print(e)
        print("❗️Error")
    except OSError as e:
        print(e)
        print("❗️Error")


def download_images_from_src_list(src_list, download_dir):
    for url in src_list:
        file_path = urljoin(url, urlparse(url).path)
        print(file_path)
        download_file_to_dir(file_path, download_dir)
        time.sleep(sleep_time_sec)


def download_images_from_url_list(url_list, download_dir):
    for url in url_list:
        print(url)
        # request にして try catch する
        req = urllib.request.Request(url)
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        src_list = [img.get("src") for img in soup.find_all("img")]
        print("Start downloading...")
        download_images_from_src_list(src_list, download_dir)
        time.sleep(sleep_time_sec)
