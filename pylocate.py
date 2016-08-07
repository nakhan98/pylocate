#!/usr/bin/env python2
"""
pylocate
----------
Quick and dirty python version of mlocate

Options:
    -u, --update                Re-index SEARCH_DIRS and update pickle store
    -f, --find <search_term>    Search SEARCH_DIRS for file using <search_term>
                                (optional)

Usage:
    ./pylocate.py -u
    ./pylocate.py -f find_me
    ./pylocate.py find_me_*.py

"""

import pickle
import os
import sys
import time
import fnmatch

SEARCH_DIRS = [
    # "/home/user/some_dir_1",
    # "/home/user/some_dir_2"
]
PICKLE_STORE = os.path.join(os.path.expanduser('~'), ".pylocate.pkl")


def get_file_paths():
    file_paths = []
    for dir_ in SEARCH_DIRS:
        print("Indexing %s..." % dir_)
        for root, directories, filenames in os.walk(dir_):
            for filename in filenames:
                file_paths.append(os.path.join(root, filename))
    return file_paths


def update_pickle_store():
    begin = time.time()
    file_paths = get_file_paths()
    with open(PICKLE_STORE, "wb") as pickle_store:
        pickle.dump(file_paths, pickle_store)
    end = time.time()
    print("Done! Indexed %d files in %.2f seconds." % (len(file_paths),
                                                       end-begin))


def load_pickle_store():
    with open(PICKLE_STORE) as pickle_store:
        return pickle.load(pickle_store)


def find_fnmatch(filename):
    begin = time.time()
    file_paths = load_pickle_store()
    count = 0
    for file_ in file_paths:
        if fnmatch.fnmatchcase(file_.split('/')[-1], filename):
            print file_
            count += 1
    end = time.time()
    print("Search took %.2f seconds - %d results (searched %d files)"
          % (end-begin, count, len(file_paths)))


def find_file(filename):
    if '*' in filename or '?' in filename:
        return find_fnmatch(filename)
    begin = time.time()
    file_paths = load_pickle_store()
    count = 0
    for file_ in file_paths:
        if filename in file_.split('/')[-1]:
            print file_
            count += 1
    end = time.time()
    print("Search took %.2f seconds - %d results (searched %d files)"
          % (end-begin, count, len(file_paths)))


def main(argv):
    if len(argv) == 2 and argv[1] in ("-u", "--update"):
        update_pickle_store()
    elif len(argv) == 2:
        find_file(argv[1])
    elif len(argv) == 3 and argv[1] in ("-f", "--find"):
        find_file(argv[2])
    else:
        print(__doc__.strip())
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
