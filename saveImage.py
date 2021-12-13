import os
import pprint
import time
import urllib.error
import urllib.request


def download_file(url, dist_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dist_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as err:
        print(err)


ß
