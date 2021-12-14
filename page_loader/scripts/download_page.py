import argparse
import sys
from pathlib import Path

import requests

from page_loader import download
from page_loader.logging import error_logger

OK_CODE = 0
NETWORK_ERROR_CODE = 1
PERMISSIONS_ERROR_CODE = 2
NONEXISTENT_OUTPUT_DIR_CODE = 3
UNKNOWN_ERROR_CODE = 4


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument(
        "-o",
        "--output",
        default=Path.cwd(),
        metavar="OUTPUT",
        help=f"output directory, default is {Path.cwd()}",
    )
    return parser.parse_args()


def handle_exception(
    exception_object: Exception, *, user_error_message: str, exit_code: int
) -> None:
    error_logger.error(str(exception_object))
    print(user_error_message)
    sys.exit(exit_code)


def main():
    args = parse_args()
    try:
        path_to_page = download(args.url, args.output)
    except requests.RequestException as exception:
        handle_exception(
            exception,
            user_error_message=f"Can't download specified page: {args.url}",
            exit_code=NETWORK_ERROR_CODE,
        )
    except FileNotFoundError as exception:
        handle_exception(
            exception,
            user_error_message=f"Output directory {args.output} doesn't exist",
            exit_code=NONEXISTENT_OUTPUT_DIR_CODE,
        )
    except PermissionError as exception:
        handle_exception(
            exception,
            user_error_message=f"Insufficient permissions for output directory {args.output}",
            exit_code=PERMISSIONS_ERROR_CODE,
        )
    except Exception as exception:
        handle_exception(
            exception,
            user_error_message=f"Something went wrong, try again...",
            exit_code=UNKNOWN_ERROR_CODE,
        )

    print(path_to_page)
    sys.exit(OK_CODE)


if __name__ == '__main__':
    main()
