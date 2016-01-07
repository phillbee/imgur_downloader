import sys
import crawler


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    crawler.crawl()


if __name__ == "__main__":
    main()
