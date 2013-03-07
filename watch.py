#!/usr/bin/env python

'''
Command line tool to watch a URL continuously and notify with a sound alert
when an update is found. Run './watch.py --help' for a list of argument
options and usage.
'''

from argparse import ArgumentParser
from datetime import datetime
from difflib import unified_diff
from sys import stderr
from time import sleep
from urllib2 import build_opener, Request, URLError
from urlparse import urlparse

# Constants.
_BASE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; '
                  'rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,'
              'text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Charset': 'ISO-8859-1',
    'Content-type': 'application/x-www-form-urlencoded',
}
_LAST_CONTENT_FILE = '/tmp/.last_content'
_DESCRIPTION = '''Watch a web page continuously and notify with a sound alert
when an update occurs.'''
_HELP1 = 'the page url to be watched'
_HELP2 = 'The interval in seconds between requests (default: 30)'
_HELP3 = 'The percentual of variation tolerance between pages (default: 0)'
_ERR1 = 'Error: did you forgot to prefix URL with "http://www." or ' \
        '"https://www."?\n'


def check_for_update(url, tolerance, header={}):
    header = dict(_BASE_HEADER, Host=urlparse(url).netloc)
    request = Request(url, None, header)
    opener = build_opener()

    try:
        res = opener.open(request)

    except URLError, e:
        print >> stderr, _ERR1
        raise(e)

    else:
        # Page's content from last request.
        with open(_LAST_CONTENT_FILE, 'r') as f:
            last = f.readlines()

        # Page's current content.
        curr = res.readlines()

        # Difference between current and last content. See
        # http://docs.python.org/2/library/difflib.html#difflib.unified_diff
        diff = list(unified_diff(last, curr, n=0))

        # Number of lines removed from last request.
        less = len([x for x in diff[2:] if x.startswith('-')])

        # Number of lines added since last request.
        plus = len([x for x in diff[2:] if x.startswith('+')])

        # Number of changed lines since last request.
        maxi = max(less, plus)

        # Try to calculate the percentage of changed lines since last request.
        try:
            perc = 100 * float(maxi) / len(last)

        # Except a division by zero if there is no previous request.
        except ZeroDivisionError:
            perc = 0

            # Store the current content to file.
            with open(_LAST_CONTENT_FILE, 'w') as f:
                f.writelines(curr)

        # Checks whether the number of lines changed is greater than tolerance.
        if perc > tolerance:
            now = datetime.now().ctime()

            print '%d%% of page has changed on %s. Diff below:' % (perc, now)
            print ''.join(diff)
            print '\a'  # Beep alert.

            # Store the current content to file.
            with open(_LAST_CONTENT_FILE, 'w') as f:
                f.writelines(curr)

if __name__ == '__main__':
    # Parse coomand line arguments.
    parser = ArgumentParser(description=_DESCRIPTION)

    parser.add_argument('url', help=_HELP1)
    parser.add_argument('-i', '--interval', metavar='I', type=int, default=30,
                        help=_HELP2)
    parser.add_argument('-t', '--tolerance', metavar='T', type=int, default=0,
                        help=_HELP3)

    args = parser.parse_args()

    # Initialize an empty file to store the content from latest request.
    open(_LAST_CONTENT_FILE, 'w+')

    # Infinitive loop for checking for updates.
    while True:
        check_for_update(args.url, args.tolerance)
        sleep(args.interval)
