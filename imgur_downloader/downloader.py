import grequests
import iterable_helper
import os
import errno

# ToDo: take path as a command line param
DOWNLOAD_PATH = 'downloaded/'


def download_images(file_names, progress_reporter=None):
    mkdir_p(DOWNLOAD_PATH)

    existing_files = set()
    for name in file_names:
        if os.path.isfile(generate_file_path(name)):
            existing_files.add(name)
    urls_to_download = ['http://i.imgur.com/' + name for name in set(file_names) - existing_files]

    downloaded = 0
    # batch the image requests, so that not too many async request calls are made at once
    for batch in iterable_helper.batch(urls_to_download, 5):
        requests = (grequests.get(url) for url in batch)
        responses = grequests.map(requests)

        for response in responses:
            path = generate_file_path(response.url.split('/')[-1])
            with open(path, 'w') as f:
                f.write(response.content)
            downloaded += 1
            if progress_reporter:
                progress_reporter(downloaded)


def generate_file_path(file_name):
    return DOWNLOAD_PATH + file_name


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
