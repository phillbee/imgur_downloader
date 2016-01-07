import sys
import runner


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    runner.run(args)

if __name__ == "__main__":
    main()
