import sys
from crawler import Crawler
import downloader
from functools import partial


def progress_reporter(items_downloaded, total_items):
    sys.stdout.write("\r{0} of {1} downloaded".format(items_downloaded, total_items))
    sys.stdout.flush()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    c = Crawler()
    file_names = [image for p in c.posts for image in p.images]

    downloader.download_images(file_names, partial(progress_reporter, total_items=len(file_names)))

if __name__ == "__main__":
    main()
