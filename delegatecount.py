#!/usr/bin/python
import sys
import curses
from operator import itemgetter

'''
Primary States for 1st Tues in March:
Alabama Primary (50 total delegates/47 bound) - Proportional with 20% threshold
Arkansas Primary (40/37) - Proportional with 15% threshold
Georgia Primary (76) - Proportional with 20% threshold
Massachusetts Primary (42/39) - Proportional with 5% threshold
Oklahoma Primary (43/40) Proportional with 15% threshold
Tennessee Primary (58/55) Proportional with 20% threshold
Texas Primary (155/152) Proportional with 20% threshold
Vermont Primary (16/13)Proportional with 20% threshold
Virginia Primary (49/46) Proportional
'''
'''
Alaska Caucuses (28/25) Proportional with 13% threshold
Minnesota Caucuses (38/35) - Proportional with 10% threshold
Wyoming Caucuses (29/0), North Dakota Caucuses(28/0)  No presidential preference poll, all delegates are officially unbound.
'''

# rules for Texas
# wta level 50%, prop thresh is 20%
# Tx district rules: 36 districts x 3 delegates.
# top > .5:  3 to top; top > .2 and < .5: 2 to top, 1 to 2nd
# top < .2: 1 each to top 3

no_cds = {}
al_cd_rule = {'state': 'Alabama', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 7}
# wta thresh - one candidate gets above that 0.2 and nobody else does = 0.2
al_state_rule = {'state': 'Alabama', 'wta': 0.5, 'wtathresh': 0.2,
                 'propthresh': 0.2, 'toptwothresh': 0.2, 'numdelegates': 26, 'minthreshsplit': 1}
ak_cd_rule = {'state': 'Alaska', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
ak_state_rule = {'state': 'Alaska', 'wta': 0.99, 'propthresh': 0.13,
                 'toptwothresh': 0.99, 'numdelegates': 25, 'minthreshsplit': 1}
ar_cd_rule = {'state': 'Arkansas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 4}
ar_state_rule = {'state': 'Arkansas', 'wta': 0.99, 'propthresh': 0.15,
                 'toptwothresh': 0.2, 'numdelegates': 25, 'minthreshsplit': 2}
ga_cd_rule = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.01,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 14}
# divide 31 proportionally and give a 3 del bonus to the top vote-getter
ga_state_rule = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.2, 'topvotedelbonus': 3,
                 'toptwothresh': 0.2, 'numdelegates': 34, 'minthreshsplit': 2}
ma_cd_rule = {'state': 'Massachusetts', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
ma_state_rule = {'state': 'Massachusetts', 'wta': 0.99, 'propthresh': 0.05,
                 'toptwothresh': 0.05, 'numdelegates': 39, 'minthreshsplit': 1}

ok_cd_rule = {'state': 'Oklahoma', 'wta': 0.5, 'propthresh': 0.15,
              'toptwothresh': 0.15, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 5}
ok_state_rule = {'state': 'Oklahoma', 'wta': 0.5, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 26, 'minthreshsplit': 2}

tn_cd_rule = {'state': 'Tennessee', 'wta': 0.667, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 9}
tn_state_rule = {'state': 'Tennessee', 'wta': 0.667, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1}
tx_cd_rule = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 36}
tx_state_rule = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
                 'toptwothresh': 0.2, 'numdelegates': 47, 'minthreshsplit': 2}
# VA no CDs
va_cd_rule = {'state': 'Virginia', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
va_state_rule = {'state': 'Virginia', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 46, 'minthreshsplit': 1}
vt_cd_rule = {'state': 'Vermont', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'numdistricts': 0}
vt_state_rule = {'state': 'Vermont', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 16, 'minthreshsplit': 1}
#ignoring rules about if nobody gets 20%, assuming someone will get 20%
# if nobody gets 20%, then the rules are the same but set at 15%, then 10%.

def delegatecount():
    return


def main():
    if (len(sys.argv) == 2):
        inputfile = sys.argv[1]
    else:
        print("usage: <program> inputfile")
        sys.exit()
    with open(inputfile) as f:
        inputlines = [x.strip('\n') for x in f.readlines()]
        votes = Votes(inputlines)
        CandList = {}
        for linenum, row in enumerate(inputlines):
            print row
            (cand, poll) = row.split(",")
            pollnum = float(poll)
            CandList[cand] = pollnum
        delswon=[]
        sumpoll=0
        print "SEC state poll:",
        for cand in CandList:
            print cand, CandList[cand]*100, "%, ",
            sumpoll +=CandList[cand]
        print "  Sum:", sumpoll
        delswon.append(votes.del_alloc_state(al_cd_rule, al_state_rule, CandList))
        delswon.append(votes.del_alloc_state(ar_cd_rule, ar_state_rule, CandList))
        delswon.append(votes.del_alloc_state(ga_cd_rule, ga_state_rule, CandList))
        delswon.append(votes.del_alloc_state(ma_cd_rule, ma_state_rule, CandList))
        delswon.append(votes.del_alloc_state(ok_cd_rule, ok_state_rule, CandList))
        delswon.append(votes.del_alloc_state(tn_cd_rule, tn_state_rule, CandList))
        delswon.append(votes.del_alloc_state(tx_cd_rule, tx_state_rule, CandList))
        delswon.append(votes.del_alloc_state(va_cd_rule, va_state_rule, CandList))
        delswon.append(votes.del_alloc_state(vt_cd_rule, vt_state_rule, CandList))
        Sum = {i:0 for i in CandList}
        for result in delswon:
            for cand in result:
                Sum[cand] += int(result[cand])
        print "SEC primary result total:", Sum
        return



class Votes():

    def __init__(self, inputlines):
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
        propthresh = rules['propthresh']
        dels = rules['numdelegates']
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
            DelList[cand[0]] = dels
            return DelList
        if dels == 3:   # CD rules
            if num_above_thresh > 0:
                DelList[cand[0]] = 2 * dels / 3
                DelList[cand[1]] = dels / 3
                return DelList
            else:
                DelList[cand[0]] = dels / 3
                DelList[cand[1]] = dels / 3
                DelList[cand[2]] = dels / 3
                return DelList
        else:  # At-large rules
            #topbonus is Georgia rule, giving top vote getter 3 at-large dels
            topbonus = 0
            if 'topvotedelbonus' in rules:
                topbonus = rules['topvotedelbonus']
                dels = dels - topbonus
            pollsum = sum(x[1] for x in pollorder[0:alloc_split])
            sumdels = 0
            # proportional among the candidates who qualify. We use rounding and then
            # addition of delegates if needed. There are variations in rounding (we ignore).
            for i in range(alloc_split):
                DelList[cand[i]] = round((poll[i] / pollsum) * dels)
                sumdels += round((poll[i] / pollsum) * dels)
                print i, cand[i], poll[i], DelList[cand[i]], sumdels, pollsum, round((poll[i] / pollsum) * dels), topbonus
            remainingdels = int(dels - sumdels)
            DelList[cand[0]] += topbonus
            for i in range(remainingdels):
                DelList[cand[i]] += 1
            return DelList

    def del_alloc_state(self, cd_rule, state_rule, CandList):
        delslist = []
        pollorder = sorted(CandList.items(), key=itemgetter(1), reverse=True)
        num_cds = cd_rule['numdistricts']
        print "\nState of", state_rule['state'], "with", num_cds * cd_rule['numdelegates'], "delegates in CDs and", state_rule['numdelegates'], "at-large delegates."
        print  "Delegates total at stake:", num_cds * cd_rule['numdelegates'] + state_rule['numdelegates']
        for i in range(num_cds):
            delswon = self.delegate_alloc(cd_rule, pollorder)
            delslist.append(delswon)
        delswon = self.delegate_alloc(state_rule, pollorder)
        delslist.append(delswon)
        Sum = {i:0 for i in CandList}
        for i in delslist:
            for key in i:
                Sum[key] += i[key]
        print Sum
        return Sum


if __name__ == '__main__':
    main()
