#!/usr/bin/python
import sys
import csv
statemap = { 'AL': 'Alabama', 'AK': 'Alaska', 'AR': 'Arkansas', 'GA': 'Georgia',
             'HI': 'Hawaii', 'ID': 'Idaho', 'KS': 'Kansas',
             'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MA': 'Massachusetts',
             'MI': 'Michigan', 'OK': 'Oklahoma', 'PR': 'PuertoRico',
             'TN': 'Tennessee', 'TX': 'Texas', 'VT': 'Vermont', 'VA': 'Virginia',
             'MN': 'Minnesota', 'WY':'Wyoming', 'MS': 'Mississippi', 'MO':'Missouri',
             'AZ': 'Arizona', 'UT':'Utah'}
# poll has
# Date
# Area - State and CD
#

def main():
    if (len(sys.argv) == 2):
        inputfile = sys.argv[1]
    elif (len(sys.argv) == 3):
        option = sys.argv[2]
        inputfile = sys.argv[2]
    else:
        print("usage: <program> inputfile")
        sys.exit()
    pollrows = read_csv(inputfile)
    read_pollrows(pollrows)
    #CandPoll = read_polls_ivr(inputfile)
    return

# Make CandPoll a dictionary of polls, for each state and CD
# Texas, TexasCD1, etc.  TexasCD1: { "Carson":0.08, "Cruz":0.05} etc.
# Date.
def read_csv(inputfile):
    with open(inputfile, 'rb') as csvfile:
        pollrows = csv.reader(csvfile, delimiter=',', quotechar='"')
        polldata=[]
        for row in pollrows:
            polldata.append(row)
            #print row
    return polldata

def read_polls_ivr(inputfile):
    with open(inputfile) as f:
        inputlines = [x.strip('\n') for x in f.readlines()]
        CandPoll = {}
        headerinfo = []
        statename ='none'

def read_pollrows(inputlines):
    for linenum, rowdata in enumerate(inputlines):
        if rowdata[0]=='Date':
            headerinfo=rowdata
            print "Location",
            for i in headerinfo[15:24]:
                print ",",i,
            print
            #for i,ind in enumerate(headerinfo):
                #print i,":",ind,
        else:
            polldata = rowdata
            if 'CD' in polldata[1]:
                pollarea = statename+polldata[1].strip()
                #print pollarea, statename, statemap[statename], polldata[1].strip()
            else:
                #print 'state match', polldata[1]
                statename = polldata[1]
                pollarea = polldata[1]
            if statename in statemap:
                print pollarea,
                for i in polldata[15:24]:
                    print ",",i,
                print
	    #print rowdata
    return


if __name__ == '__main__':
    main()
