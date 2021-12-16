import os
import time
import pathlib
import validators
import urllib.error
import urllib.request
import base64

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

sleep_time_sec = 200 / 1000


def create_basic_auth_header(user, password):
    basic_user_and_pasword = base64.b64encode(
        "{}:{}".format(user, password).encode("utf-8")
    )
    return "Basic " + basic_user_and_pasword.decode("utf-8")


def download_file_to_dir(src, dist_dir):
    download_path = pathlib.Path(dist_dir + os.path.dirname(urlparse(src).path))
    download_path.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(src) as web_file, open(
            os.path.join(download_path, os.path.basename(src)), "wb"
        ) as local_file:
            print("...downloading to", download_path)
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
        print(file_path)
        if validators.url(file_path):
            parsedUrl = urlparse(url)
            download_file_to_dir(
                file_path, download_dir + "/" + parsedUrl.netloc + parsedUrl.path
            )
            print("download done")
            time.sleep(sleep_time_sec)
        else:
            print("❗️Error: 画像のパスが不正です")


def download_images_from_url_list(url_list, download_dir, user, password):
    for url in url_list:
        print("access to ", url)
        if validators.url(url):
            if user != "" and password != "":
                req = urllib.request.Request(
                    url,
                    headers={"Authorization": create_basic_auth_header(user, password)},
                )
            else:
                req = urllib.request.Request(url)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, "html.parser")
            src_list = list(set([img.get("src") for img in soup.find_all("img")]))
            print("start downloading...")
            download_images_from_src_list(url, src_list, download_dir)
            time.sleep(sleep_time_sec)
        else:
            print("❗️Error: 画像取得元 URL が不正です")

    print("✨ Finished ✨")
