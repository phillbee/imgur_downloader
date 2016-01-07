Imgur downloader
================

A quick proof of concept project that will scrape the main page of imgur and download the images, filtered on
number of points, number of views or topic.

Usage
-----

You can install from the root directory:

    python setup.py install

Then run:

    imgur_downloader --points 500

Or run with `python -m`:

    python -m imgur_downloader --views 100000

Command line parameters
-----------------------

    usage: imgur_downloader [-h] [--points POINTS] [--views VIEWS] [--topic TOPIC]

    Download some images from imgur, based on specified criteria

    optional arguments:
      -h, --help       show this help message and exit
      --points POINTS  minimum number of points a post must have to download
      --views VIEWS    minimum number of views a post must have to download
      --topic TOPIC    specific topic to download
