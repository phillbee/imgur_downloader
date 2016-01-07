import requests
import grequests
import sys
from models import Post
from models import StartingPage
import urlparse
import iterable_helper


class Crawler(object):
    IMGUR_BASE_URL = 'http://imgur.com'

    def __init__(self, options, url_path='hot/time'):
        self.options = options
        self.url_path = url_path
        self.visited_links = set()
        self.posts = list()
        self._crawl(options)

    def _crawl(self, options):
        # ToDo: allow more than just the images that are initially loaded on imgur
        starting_page_url = urlparse.urljoin(self.IMGUR_BASE_URL, self.url_path)
        starting_page_response = requests.get(starting_page_url)
        starting_page = StartingPage(starting_page_response)

        if not starting_page.links:
            sys.exit('No posts found on the specified starting page')

        # batch the links, so that not too many async request calls are made at once
        for link_batch in iterable_helper.batch(starting_page.links, 5):
            # ToDo: replace the set membership testing with a bloom filter when urls are persisted between runs
            new_links = filter(lambda l: l not in self.visited_links, link_batch)
            rs = (grequests.get(link) for link in new_links)
            responses = grequests.map(rs)

            while len(responses):
                response = responses.pop()
                post = Post(response)
                self.visited_links.add(post.url)

                if self._meets_criteria(post):
                    self.posts.append(post)

    def _meets_criteria(self, post):
        if self.options.points and post.points < int(self.options.points):
            return False
        if self.options.views and post.views < int(self.options.views):
            return False
        if self.options.topic and post.topic != self.options.topic:
            return False
        return True
