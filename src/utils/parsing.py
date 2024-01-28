import re
from os import listdir
from os.path import isfile, join

from utils.constants import EARNINGS_CALLS_FILENAME_REGEX, EARNINGS_CALLS_REL_DIRNAME


def parse_earnings_calls(dirname: str = EARNINGS_CALLS_REL_DIRNAME):
    """Parses a list of earnings calls into their components.

    Args:
        dirname (str): The directory containing the earnings calls.

    Returns:
        dict: A dictionary of company stock symbol to a list of its earnings calls files.
    """

    mapping = {}
    for filename in listdir(dirname):
        file_path = join(dirname, filename)
        if not isfile(file_path):
            raise ValueError("Invalid filename: {}".format(filename))

        stock_symbol, _, _, _ = parse_filename(filename, EARNINGS_CALLS_FILENAME_REGEX)
        if stock_symbol not in mapping:
            mapping[stock_symbol] = []

        mapping[stock_symbol].append(file_path)

    return mapping


def parse_filename(filename: str, regex: str):
    """Parses a filename into its components.

    Args:
        filename (str): The filename to parse.
        regex (str): The regex string to parse with.

    Returns:
        tuple: A tuple containing the components of the filename.
    """
    match = re.match(regex, filename)
    if match is None:
        raise ValueError("Invalid filename: {}".format(filename))

    return match.groups()
