import os
import requests
from app.service.global_data import g


def download_thread(url, path, filename, finish):
    if filename in g['downloading']:
        return

    g['downloading'][filename] = True
    download_file(url, path, filename)

    g['downloading'].pop(filename)
    finish['done'] = True


def download_file(url, path, filename, chunk_size=4*1024):
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, filename)
    full_path_download = full_path + '.download'

    with requests.get(url, stream=True) as req:
        with open(full_path_download, 'wb') as f:
            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    try:
        os.rename(full_path_download, full_path)
    except:
        pass


def write_thread(path, filename, content):
    if filename in g['writing']:
        return

    if not os.path.exists(path):
        os.makedirs(path)

    full_path = os.path.join(path, filename)
    with open(full_path, 'wb') as file:
        file.write(content)

    g['writing'].pop(filename)
