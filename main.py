import os
import datetime
import logging
import tempfile
import sys
from argparse import ArgumentParser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


EDGAR_PREFIX = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/{}.zip"
FILENAME_PREFIX = "{}q{}"

"https://www.sec.gov/files/node/add/data_distribution/2020q1.zip"

def _get_current_quarter():
    return "QTR%s" % ((datetime.date.today().month - 1) // 3 + 1)


def _quarterly_idx_list(dest, since_year=1993):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    logging.debug("downloading files since %s" % since_year)
    years = range(since_year, datetime.date.today().year + 1)
    for year in years:
        for quarter in range(4):
            filename = FILENAME_PREFIX.format(year, quarter + 1)
            url = EDGAR_PREFIX.format(filename)
            print(url)
            import requests
            r = requests.get(url, allow_redirects=True)
            open(os.path.join(dest, filename + ".zip"), 'wb').write(r.content)


def download(dest, since_year=1993):
    idxes = _quarterly_idx_list(dest, since_year)
    print(idxes)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-y",
        "--from-year",
        type=int,
        dest="year",
        help="The year from which to start downloading "
        + "the filing index. Default to current year",
        default=datetime.date.today().year,
    )

    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="A directory where the filing index files will"
        + "be downloaded to. Default to a temporary directory",
        default=tempfile.mkdtemp(),
    )

    args = parser.parse_args()

    logger.debug("downloads will be saved to %s" % args.directory)
    logger.debug("downloads starting from %s" % args.year)
    download(args.directory, args.year)

    logger.info("Files downloaded in %s" % args.directory)
