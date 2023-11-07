#!/usr/bin/env python
import argparse
import os
import sys


class TailError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


def check_file_validity(file_: str):
    if not os.access(file_, os.F_OK):
        raise TailError("File '%s' does not exist" % file_)
    if not os.access(file_, os.R_OK):
        raise TailError("File '%s' not readable" % file_)
    if os.path.isdir(file_):
        raise TailError("File '%s' is a directory" % file_)


class Util:
    def __init__(self, tailed_file: str):
        check_file_validity(tailed_file)
        self.target_file = tailed_file
        self.callback = sys.stdout.write

    def follow(self, n: int = 5):
        if n < 1:
            return
        with open(self.target_file, 'r') as file:
            file.seek(0, os.SEEK_END)
            position = file.tell()
            lines_seen = 0
            if file.read(1) == '\n':
                position -= 1
                file.seek(position)
            while lines_seen < n and file.tell() > 0:
                c = file.read(1)
                if c == '\n':
                    lines_seen += 1
                    if lines_seen == n:
                        break
                position -= 2
                file.seek(position)
            self.callback(file.read())

    def register_callback(self, func):
        self.callback = func


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('-n', "--number", type=int, default=None)
    args = parser.parse_args()
    util = Util(args.file)
    util.follow(args.number)
