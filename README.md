# pylocate
----------
Quick and dirty python version of mlocate

Options:
    -u, --update Re-index       SEARCH_DIRS and update pickle store
    -f, --find <search_term>    Search directories for file using <search_term>
                                (optional)

Usage:
    ./pylocate.py -u
    ./pylocate.py -f find_me
    ./pylocate.py find_me_*.py
