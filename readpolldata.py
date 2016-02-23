#!/usr/bin/python
from __future__ import print_function
import sys
import csv
statemap = { 'AL': 'Alabama', 'AK': 'Alaska', 'AR': 'Arkansas', 'GA': 'Georgia',
             'HI': 'Hawaii', 'ID': 'Idaho', 'KS': 'Kansas',
             'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MA': 'Massachusetts',
             'MI': 'Michigan', 'OK': 'Oklahoma', 'PR': 'PuertoRico',
             'TN': 'Tennessee', 'TX': 'Texas', 'VT': 'Vermont', 'VA': 'Virginia',
             'MN': 'Minnesota', 'WY':'Wyoming', 'MS': 'Mississippi', 'MO':'Missouri',
             'AZ': 'Arizona', 'UT':'Utah'}

def p2f(x):
    if "%" in x:
        return str(float(x.strip('%'))/100)
    elif "," in x:
        return str(int(x.replace(",",'')))
    else:
        return x

# Make CandPoll a dictionary of polls, for each state and CD
# Texas, TexasCD1, etc.  TexasCD1: { "Carson":0.08, "Cruz":0.05} etc.
# Date.
def read_ivr_csv(inputfile):
    with open(inputfile, 'rb') as csvfile:
        pollrows = csv.reader(csvfile, delimiter=',', quotechar='"')
        polldata=[]
        for row in pollrows:
            polldata.append(row)
    return polldata

def read_pollrows(inputlines):
    CandPoll={}
    for linenum, rowdata in enumerate(inputlines):
        if rowdata[0]=='Date':
            headerinfo=rowdata
            print("Location,",end=" ")
            print(", ".join(headerinfo[15:24]))
            pollkey = headerinfo[15:24]
        else:
            if 'CD' in rowdata[1]:
                pollarea = statename+rowdata[1].strip()
                #print pollarea, statename, statemap[statename], polldata[1].strip()
            else:
                #print 'state match', polldata[1]
                pollarea = statename = rowdata[1]
            if statename in statemap:
                polldata = list(map(p2f, rowdata[15:24]))
                if polldata[5] !='':
                    print(pollarea,end="")
                    print(",",", ".join(polldata))
                CandPoll[pollarea] = {pollkey[i]:polldata[i] for i in xrange(len(pollkey))}
    return CandPoll


    # Make CandPoll a dictionary of polls, for each state and CD
    # Texas, TexasCD1, etc.  TexasCD1: { "Carson":0.08, "Cruz":0.05} etc.
    # Our 'standard' format:
    # Location, Date, n, Bush, Carson, Cruz, Kasich, Rubio, Trump, Und
    # TNCD9, 18-Feb, 528, 0.09, 0.06, 0.2, 0.08, 0.09, 0.3, 0.15
def read_polls_standard(inputfile):
    with open(inputfile) as f:
        inputlines = [x.strip('\n') for x in f.readlines()]
        CandPoll = {}
        #print(inputlines)
        for linenum, row in enumerate(inputlines):
            print(row)
            rowlist = row.split(",")
            if rowlist[0]=="Location":
                candlist=[i.strip(" ") for i in rowlist[3:]]
            else:
                CandPoll[rowlist[0]] = {candlist[i]:float(rowlist[i+3].strip(" ")) for i in xrange(len(rowlist[3:])-1)}
        sumpoll=0
        print("Full state poll results:")
        for state in CandPoll:
            print(state, CandPoll[state])
        print(CandPoll)
    return candlist, CandPoll

def read_polls_basic(inputfile):
    with open(inputfile) as f:
        inputlines = [x.strip('\n') for x in f.readlines()]
        CandPoll = {}
        for linenum, row in enumerate(inputlines):
            #print row
            (cand, poll) = row.split(",")
            pollnum = float(poll)
            CandPoll[cand] = pollnum
        sumpoll=0
        print("Basic poll result:")
        for cand in CandPoll:
            print(cand, CandPoll[cand]*100, "%, ")
            sumpoll +=CandPoll[cand]
        print("  Sum:", sumpoll)
    return CandPoll
'''
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
'''
