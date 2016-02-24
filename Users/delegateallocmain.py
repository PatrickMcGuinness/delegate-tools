#!/usr/bin/python
import sys
import curses
from operator import itemgetter
from delegaterules import *
from readpolldata import *
from delegatealloc import *


statemap = { 'AL': 'Alabama', 'AK': 'Alaska', 'AR': 'Arkansas', 'GA': 'Georgia',
             'HI': 'Hawaii', 'ID': 'Idaho', 'KS': 'Kansas',
             'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MA': 'Massachusetts',
             'MI': 'Michigan', 'OK': 'Oklahoma', 'PR': 'PuertoRico',
             'TN': 'Tennessee', 'TX': 'Texas', 'VT': 'Vermont', 'VA': 'Virginia',
             'MN': 'Minnesota', 'WY':'Wyoming', 'MS': 'Mississippi', 'MO':'Missouri',
             'AZ': 'Arizona', 'UT':'Utah'}


def main():
    if (len(sys.argv) == 2):
        inputfile = sys.argv[1]
    else:
        print("usage: <program> inputfile")
        sys.exit()
    votes = Delegates()
    allPolls={}
    cand_list = []
    (cand_list, allPolls) = read_polls_standard(inputfile)
    delswon=[]
    for state in statemap:
        if state in allPolls:
            state_polls={}
            for loc in allPolls:   # can be either state (VA) or CD, ie MNCD3
                if state in loc:
                    state_polls[loc]=allPolls[loc]
            # print state, delegaterule[state]
            # find all the polls matching StateCD
            delswon.append(votes.alloc_delegates(state, delegaterule[state], allPolls[state],
                            delegatecdrule[state],  state_polls))
        print "done with", state
    Sum = {i:0 for i in cand_list}
    for stateres in delswon:
        for result in stateres:
            for cand in stateres[result]:
                Sum[cand] += int(stateres[result][cand])
    print delswon
    print "SEC primary result total:", Sum
    return


if __name__ == '__main__':
    main()
