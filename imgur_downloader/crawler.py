import requests
import grequests
import sys
from models import Post
from models import StartingPage
import urlparse
import iterable_helper

class Crawler:
    IMGUR_BASE_URL = 'http://imgur.com'

    def __init__(self, url_path='hot/time'):
        self.url_path = url_path
        self.visited_links = set()
        self.posts = list()
        self._crawl()

    def _crawl(self):

        # ToDo: allow more than just the images that are initially loaded on imgur
        starting_page_url = urlparse.urljoin(self.IMGUR_BASE_URL, self.url_path)
        starting_page_response = requests.get(starting_page_url)
        starting_page = StartingPage(starting_page_response)

        if not starting_page.links:
            sys.exit('No posts found on the specified starting page')

        # batch the links, so that not too many async request calls are made at once
        for link_batch in iterable_helper.batch(starting_page.links, 5):
            rs = (grequests.get(link) for link in link_batch)
            responses = grequests.map(rs)

            while len(responses):
                response = responses.pop()

                post = Post(response)
                self.posts.append(post)

                #print post.url.ljust(32) + " | " + (str(len(post.image_urls)) + " images").rjust(9) + " | " + \
                #      (str(post.points) + " points").rjust(15) + " | " + \
                #      (str(post.views) + " views").rjust(14 ) + " | " + post.topic.ljust(17) + " | "
                self.visited_links.add(post.url)
