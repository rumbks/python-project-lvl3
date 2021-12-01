import argparse
import sys

import requests

from page_loader import download
from page_loader.logging import error_logger

OK_CODE = 0
NETWORK_ERROR_CODE = 1
PERMISSIONS_ERROR_CODE = 2
NONEXISTENT_OUTPUT_DIR_CODE = 3


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
    try:
        path_to_page = download(args.url, args.output)
    except requests.RequestException as error:
        error_logger.error(str(error))
        sys.exit(NETWORK_ERROR_CODE)
    except FileNotFoundError as error:
        error_logger.error(str(error))
        sys.exit(NONEXISTENT_OUTPUT_DIR_CODE)
    except PermissionError as error:
        error_logger.error(str(error))
        sys.exit(PERMISSIONS_ERROR_CODE)
    print(path_to_page)
    sys.exit(OK_CODE)


if __name__ == '__main__':
    main()
