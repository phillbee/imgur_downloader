import requests
import grequests
import sys
from models import Post
from models import StartingPage
import urlparse


# http://stackoverflow.com/a/8290508/296298
def __batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def crawl():
    starting_page_response = requests.get('http://imgur.com')
    starting_page = StartingPage(starting_page_response)

    if not starting_page.links:
        sys.exit('No posts found on the specified starting page')

    # batch the links, so that not too many async request calls are made at once
    for link_batch in __batch(starting_page.links, 5):
        rs = (grequests.get(link) for link in link_batch)
        responses = grequests.map(rs)
        visited_links = set()

        while len(responses):
            response = responses.pop()

            post = Post(response)

            print post.url.ljust(32) + " | " + (str(len(post.image_urls)) + " images").rjust(9) + " | " + \
                  (str(post.points) + " points").rjust(15) + " | " + \
                  (str(post.views) + " views").rjust(14 ) + " | " + post.topic.ljust(17) + " | "
            visited_links.add(post.url)