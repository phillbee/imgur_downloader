import sys
from crawler import Crawler
import downloader
from functools import partial
from models import Post
import argparse


def progress_reporter(items_downloaded, total_items):
    sys.stdout.write('\r{0} of {1} downloaded'.format(items_downloaded, total_items))
    sys.stdout.flush()


def run(args):
    options = configure_arg_parser(args)

    c = Crawler(options)
    Post.to_csv(c.posts)

    file_names = [image for p in c.posts for image in p.images]
    downloader.download_images(file_names, partial(progress_reporter, total_items=len(file_names)))


def configure_arg_parser(args):
    parser = argparse.ArgumentParser(description='Download some images from imgur, based on specified criteria',
                                     prog='imgur_downloader')
    parser.add_argument('--points', help='minimum number of points a post must have to download')
    parser.add_argument('--views', help='minimum number of views a post must have to download')
    parser.add_argument('--topic', help='specific topic to download')

    return parser.parse_args()