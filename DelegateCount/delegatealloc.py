#!/usr/bin/python
import sys
import curses
from operator import itemgetter
from delegaterules import *
from readpolldata import *

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


class Delegates():

    def __init__(self):
        return

# WTA rule: If a cand > WTA gets all delegates
# propthresh rule: If a candidate > propthresh, then proportionally to all candidates > thresh, shared by at least minthreshsplit
# minthreshsplit can be 1 (if only one candidate is above the threshold, they get all delegates), or 2 (texas rules)
# Fail to meet propthresh: If all candidates are < propthresh, then proportionally for all candidates
# We take out boundtotopvote dels from the at-large pool and assign it to
# top vote getter. (GA rules)
#CD rules: 3 dels - if top > WTA, 3 to top, if top > propthresh, 2 to top, 1 to next
# else 1 to the top 3 each

    def delegate_alloc(self, rules, pollorder):
        # print "in delegate_alloc"
        propthresh = rules['propthresh']
        total_dels = rules['numdelegates']
        min_thresh_split = rules['minthreshsplit']
        DelList = {}
        # print pollorder, dels
        cand = [0] * len(pollorder)
        poll = [0] * len(pollorder)
        for i in range(len(pollorder)):
            (cand[i], poll[i]) = pollorder[i]
        num_above_thresh = sum(x[1] > propthresh for x in pollorder)
        if num_above_thresh > 0:
            alloc_split = max(min_thresh_split, num_above_thresh)
        else:
            alloc_split = len(pollorder)
        # polling_sum = sum(x for x in poll)
        # print "num candidates:", len(pollorder), "num above threshold:",
        # num_above_thresh, "sum of polling:", polling_sum
        if poll[0] > rules['wta']:
            DelList[cand[0]] = total_dels
            return DelList
        if total_dels == 3:   # CD rules
            if num_above_thresh > 0:
                DelList[cand[0]] = 2 * total_dels / 3
                DelList[cand[1]] = total_dels / 3
                return DelList
            else:
                DelList[cand[0]] = total_dels / 3
                DelList[cand[1]] = total_dels / 3
                DelList[cand[2]] = total_dels / 3
                return DelList
        else:  # At-large rules
            #topbonus is Georgia rule, giving top vote getter 3 at-large dels
            topbonus = 0
            if 'topvotedelbonus' in rules:
                topbonus = rules['topvotedelbonus']
                total_dels = total_dels - topbonus
            pollsum = sum(x[1] for x in pollorder[0:alloc_split])
            sumdels = 0
            # proportional among the candidates who qualify. We use rounding and then
            # addition of delegates if needed. There are variations in rounding (we ignore).
            for i in range(alloc_split):
                DelList[cand[i]] = round((poll[i] / pollsum) * total_dels)
                sumdels += round((poll[i] / pollsum) * total_dels)
                #print i, cand[i], poll[i], DelList[cand[i]],sumdels, pollsum,
                # print round((poll[i] / pollsum) * total_dels), topbonus
            remainingdels = int(total_dels - sumdels)
            DelList[cand[0]] += topbonus
            for i in range(remainingdels):
                DelList[cand[i]] += 1
            return DelList

#CandPoll is a state poll
    def alloc_delegates(self, state_code, state_rule, statewide_poll, cd_rule, state_polls ):
        delslist = {}
        pollorder = sorted(statewide_poll.items(), key=itemgetter(1), reverse=True)
        num_cds = cd_rule['numdistricts']
        print "\nState of", state_rule['state'], "delegates:", num_cds * cd_rule['numdelegates'], "delegates in CDs and", state_rule['numdelegates'], "at-large delegates,",
        print num_cds * cd_rule['numdelegates'] + state_rule['numdelegates'], "total delegates."
        # state delegate allocations
        print pollorder
        delswon = self.delegate_alloc(state_rule, pollorder)
        delslist[state_code]=delswon

        # Do we allocate by CDs?
        if state_rule['allocbycd']==True:
            print "Alloc by CD for ", num_cds, "districts"
            for i in range(1,num_cds+1):
                loc = state_code + "CD" + str(i)
                if loc in state_polls:
                    print loc, 'found in state poll'
                    cdpollorder = sorted(state_polls[loc].items(), key=itemgetter(1), reverse=True)
                else:   # use statewide poll if there is no CD poll
                    print "no CD poll found for", loc, "in", state_polls
                    cdpollorder = pollorder
                print cdpollorder
                delswon = self.delegate_alloc(cd_rule, cdpollorder)
                delslist[loc]=delswon
        else:
            print "No allocation by CD for", state_rule['state']
        print delslist
        Sum = {i:0 for i in statewide_poll}
        for result in delslist:
            print result
            for cand in delslist[result]:
                Sum[cand] += delslist[result][cand]
        print state_rule['state'], "delegates awarded:", Sum
        return delslist


if __name__ == '__main__':
    main()
