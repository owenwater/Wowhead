#!/usr/bin/python
# encoding: utf-8

import sys
import math
from main import arg_separator
import webbrowser

def open_url(arg, index):
    url_list = arg.split(arg_separator)
    if not url_list[index]:
        index += 1
    print url_list[index]
    webbrowser.open_new_tab(url_list[index])


if __name__ == "__main__":
    open_url('http://www.google.com#www.wowhead.com', 0)
