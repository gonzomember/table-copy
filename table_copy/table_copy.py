#! /usr/bin/env python
import argparse

import MySQLdb as mysql


def copy_titles(source, target):
    """This function copies the actual data.
    """
    # set up two connections
    with mysql.connect(*source) as source, mysql.connect(*target) as target:
        source.execute('select * from titles')  # run the select query
        # iterate over the results by fetching every row from the result set
        # one by one
        for row in (source.fetchone() for n in xrange(source.rowcount)):
            # run the insert query with each fetched row
            target.execute('insert into titles values (%s, %s, %s, %s)', row)


def make_parser():
    """This function creates and configures the command line arguments parser.
    """
    parser = argparse.ArgumentParser()
    source = parser.add_argument_group('Source', 'Connection parameters for '
                                       'the source database server.')
    target = parser.add_argument_group('Target', 'Connection parameters for '
                                       'the target database server.')
    source.add_argument('--source', nargs=4, required=True,
                        metavar=('host', 'user', 'passwd', 'db'))
    target.add_argument('--target', nargs=4, required=True,
                        metavar=('host', 'user', 'passwd', 'db'))
    return parser


def main():
    """This function gets run when the script is invoked.
    """
    parser = make_parser()
    args = parser.parse_args()
    copy_titles(args.source, args.target)

if __name__ == '__main__':
    main()
