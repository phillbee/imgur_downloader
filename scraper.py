import requests
import grequests
from lxml import html
import sys
import urlparse


# http://stackoverflow.com/a/8290508/296298
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

starting_page_response = requests.get('http://imgur.com')
starting_page_parsed_body = html.fromstring(starting_page_response.content)

# Grab links to all images displayed (at least, for the moment) on the first page
links = starting_page_parsed_body.xpath('//*[@class="post"]/a/@href')
if not links:
    sys.exit('Found images found')

links = [urlparse.urljoin(starting_page_response.url, url) for url in links]

# batch the links, so that not too many async request calls are made at once
for link_batch in batch(links, 5):
    rs = (grequests.get(link) for link in link_batch)
    responses = grequests.map(rs)
    visited_links = set()

    while len(responses):
        response = responses.pop()
        parsed = html.fromstring(response.content)

        img_urls = parsed.xpath('//*[@class="post-image"]/a/@href')
        if not img_urls:
            img_urls = parsed.xpath('//*[@class="post-image"]/img/@src')
        if not img_urls:
            video_container_scripts = parsed.xpath('//*[@class="video-container"]/script/text()')
            img_urls = []
            for script in video_container_scripts:
                gif_url_start = script.index('gifUrl')
                start_quote = script.index("'", gif_url_start)
                end_quote = script.index("'", start_quote + 1)
                gif_url = script[start_quote + 1 : end_quote]
                img_urls.append(gif_url)
        img_urls = [urlparse.urljoin(starting_page_response.url, url) for url in img_urls]

        points = int(parsed.xpath('//*[@id="under-image"]/div/div[1]/div[1]/span[1]/text()')[0].translate(None, ','))
        views = int(parsed.xpath('//*[@id="under-image"]/div/div[1]/div[2]/span[1]/text()')[0].translate(None, ','))
        topic = parsed.xpath('//*[@id="topic"]/text()')
        if len(topic) == 1:
            topic = topic[0]
        else:
            topic = ""

        print response.url.ljust(32) + " | " + (str(len(img_urls)) + " images").rjust(9) + " | " + \
              (str(points) + " points").rjust(15) + " | " + \
              (str(views) + " views").rjust(14 ) + " | " + topic.ljust(17) + " | "
        visited_links.add(url)