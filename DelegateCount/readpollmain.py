#!/usr/bin/python
from __future__ import print_function
import sys
import csv
from readpolldata import *

def main():
    if (len(sys.argv) == 2):
        inputfile = sys.argv[1]
    elif (len(sys.argv) == 3):
        option = sys.argv[1]
        inputfile = sys.argv[2]
    else:
        print("usage: <program> <option> inputfile")
        sys.exit()
    if option and option == 'ivr':
        pollrows = read_ivr_csv(inputfile)
        CandPoll = read_pollrows(pollrows)
    return

if __name__ == '__main__':
    main()
