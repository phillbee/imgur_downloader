from lxml import html
import urlparse
import csv


class StartingPage(object):
    def __init__(self, response):
        parsed = html.fromstring(response.content)
        links = parsed.xpath('//*[@class="post"]/a/@href')
        if links:
            self.links = [urlparse.urljoin(response.url, url) for url in links]


class Post(object):
    def __init__(self, response):
        parsed = html.fromstring(response.content)

        self.title = parsed.xpath('//*[@class="post-title"]/text()')
        self.url = response.url.ljust(32)
        self.points = int(parsed.xpath('//*[@id="under-image"]/div/div[1]/div[1]/span[1]/text()')[0].translate(None, ','))
        self.views = int(parsed.xpath('//*[@id="under-image"]/div/div[1]/div[2]/span[1]/text()')[0].translate(None, ','))
        self.topic = parsed.xpath('//*[@id="topic"]/text()')
        if len(self.topic) == 1:
            self.topic = self.topic[0]
        else:
            self.topic = ""
        self.images = self._find_image_names(parsed)

    @staticmethod
    def _find_image_names(parsed):
        image_urls = parsed.xpath('//*[@class="post-image"]/a/@href')
        if not image_urls:
            image_urls = parsed.xpath('//*[@class="post-image"]/img/@src')
        if not image_urls:
            video_container_scripts = parsed.xpath('//*[@class="video-container"]/script/text()')
            image_urls = []
            for script in video_container_scripts:
                gif_url_start = script.index('gifUrl')
                start_quote = script.index("'", gif_url_start)
                end_quote = script.index("'", start_quote + 1)
                gif_url = script[start_quote + 1: end_quote]
                image_urls.append(gif_url)
        return [url.split('/')[-1] for url in image_urls]

    @staticmethod
    def to_csv(posts, csv_path='metadata.csv'):
        # ToDo: make csv_path a command line parameter
        with open(csv_path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(('title', 'url', 'image_count', 'points', 'views', 'topic'))

            for post in posts:
                writer.writerow((post.title, post.url, len(post.images), post.points, post.views, post.topic))
