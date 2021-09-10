import argparse

from page_loader import download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        metavar="OUTPUT",
        help="output directory",
    )
    args = parser.parse_args()
    path_to_page = download(args.url, args.output)
    print(path_to_page)


if __name__ == '__main__':
    main()
