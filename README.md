Page Watcher
============
Command line tool to watch a URL continuously and notify with a sound alert
when an update is found.

Usage
-----
**watch** [-h] [-i I] [-t T] url

Arguments
---------
      url                  the page url to be watched
      -h, --help           show this help message and exit
      -i I, --interval I   The interval in seconds between requests (default: 30)
      -t T, --tolerance T  The percentual of variation tolerance between pages
                           (default: 0)

Installation
------------
For OS X users:
`sudo curl https://raw.github.com/eduardomb/page-watcher/master/watch.py -o /opt/local/bin/watch`
`sudo chmod +x /opt/local/bin/watch`

For Linux users:
`sudo wget https://raw.github.com/eduardomb/page-watcher/master/watch.py -O /usr/local/bin/watch`
`sudo chmod +x /usr/local/bin/watch`

Examples
--------
Watch NyTimes.
`watch http://www.nytimes.com/`

Watch NyTimes but only notifies if more than 10% of the page has changed.
`watch http://www.nytimes.com/ --tolerance 10`

Watch NyTimes making requests in every 5 seconds.
`watch http://www.nytimes.com/ --interval 5`
