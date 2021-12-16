import os
import time
import pathlib
import urllib.error
import validators
import urllib.request


from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

sleep_time_sec = 100 / 1000


def download_file_to_dir(src, download_dir):
    download_path = pathlib.Path(download_dir + os.path.dirname(urlparse(src).path))
    download_path.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(src) as web_file, open(
            os.path.join(download_path, os.path.basename(src)), "wb"
        ) as local_file:
            local_file.write(web_file.read())
            print("✅ Saved")
    except urllib.error.URLError as e:
        print(e)
        print("❗️Errord")
    except OSError as e:
        print(e)
        print("❗️Error")


def download_images_from_src_list(url, src_list, download_dir):
    for src in src_list:
        file_path = urljoin(urljoin(url, src), urlparse(src).path)
        print("file_path", file_path)
        if validators.url(file_path):
            download_file_to_dir(file_path, download_dir)
            print("download done")
            time.sleep(sleep_time_sec)
        else:
            print("❗️Error: 画像のパスが不正です")


def download_images_from_url_list(url_list, download_dir):
    for url in url_list:
        print("access to ", url)
        if validators.url(url):
            # request にして try catch する
            req = urllib.request.Request(url)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, "html.parser")
            src_list = list(set([img.get("src") for img in soup.find_all("amp-img")]))
            print("start downloading...")
            download_images_from_src_list(url, src_list, download_dir)
            time.sleep(sleep_time_sec)
        else:
            print("❗️Error: 画像取得元 URL が不正です")

    print("✨ Finished ✨")
