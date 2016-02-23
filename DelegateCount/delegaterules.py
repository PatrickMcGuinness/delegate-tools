#!/usr/bin/python
import sys
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
Alaska Caucuses (28/25) Proportional with 13% threshold
Minnesota Caucuses (38/35) - Proportional with 10% threshold
Wyoming Caucuses (29/0), North Dakota Caucuses(28/0)  No presidential preference poll, all delegates are officially unbound.

March 5, 2016 (145 bound delegates)
    Kansas Caucuses (40)  Proportional with 10% threshold
    Kentucky Caucuses (45/42)  Proportional with 5% threshold
    Louisiana Primary (46/43) Proportional with 20% threshold statewide, no threshold for congressional district delegates
    Maine Caucuses (23/20)  Proportional with 10% threshold

March 6, 2016 (23 bound delegates)
    Puerto Rico Primary (23)  Proportional with 20% threshold

March 8, 2016 (140 bound delegates)
    Hawaii Caucuses (19/16)  Proportional - rounding
    Idaho Primary (32) Proportional with 20% threshold
    Michigan Primary (59/56) Proportional with 15% threshold - rounding up/down
    Mississippi Primary (39/36) Proportional with 15% threshold

March 12, 2016 (19 bound delegates)
    District of Columbia Convention (19) Proportional with 15% threshold

Super Tuesday: March 15, 2016 (361 bound delegates)
    Florida Primary (99)  Winner take all
    Illinois Primary (69)  Statewide delegates are winner take all, congressional district delegates elected directly on ballot and bound as they declare
    Missouri Primary (52/49)  Winner take all above 50%, otherwise winter take all by congressional district
    North Carolina Primary (72/69)  Proportional
    Northern Mariana Islands Caucuses (9) Winner take all
    Ohio Primary (66) Winner take all

March 19, 2016 (9 bound delegates)
    U.S. Virgin Islands (9) Winner take all

March 22, 2016 (107 bound delegates)
    American Samoa Convention (9) Delegates elected and bound at convention
    Arizona Primary (58) Winner take all
    Utah Caucuses (40)Proportional with 15% threshold
'''

# rules for Texas
# wta level 50%, prop thresh is 20%
# Tx district rules: 36 districts x 3 delegates.
# top > .5:  3 to top; top > .2 and < .5: 2 to top, 1 to 2nd
# top < .2: 1 each to top 3
# Definitions:
# wta = winner-take-all level for district or state. A winner-take-all state has wta=0.01
# wtathresh = if only one candidate is above that level, they are winner-take-all winner-take-all
# propthesh = proportional threshold

no_cds = {}
delegaterule={}
delegatecdrule={}
delegaterule['AL'] = {'state': 'Alabama', 'wta': 0.5, 'wtathresh': 0.2,
                 'propthresh': 0.2, 'toptwothresh': 0.2, 'numdelegates': 26, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['AL'] = {'wta': 0.5, 'propthresh': 0.2, 'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 7}
# wta thresh - one candidate gets above that 0.2 and nobody else does = 0.2
delegatecdrule['AK'] = {'state': 'Alaska', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule['AK'] = {'state': 'Alaska', 'wta': 0.99, 'propthresh': 0.13,'allocbycd' : True,
                 'toptwothresh': 0.99, 'numdelegates': 25, 'minthreshsplit': 1}
delegatecdrule['AR'] = {'state': 'Arkansas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 4}
delegaterule['AR'] = {'state': 'Arkansas', 'wta': 0.99, 'propthresh': 0.15,
                 'toptwothresh': 0.2, 'numdelegates': 25, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['GA'] = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.01,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 14}
# divide 31 proportionally and give a 3 del bonus to the top vote-getter
delegaterule['GA'] = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.2, 'topvotedelbonus': 3,
                 'toptwothresh': 0.2, 'numdelegates': 34, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['MA'] = {'state': 'Massachusetts', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule['MA'] = {'state': 'Massachusetts', 'wta': 0.99, 'propthresh': 0.05,
                 'toptwothresh': 0.05, 'numdelegates': 39, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['OK'] = {'state': 'Oklahoma', 'wta': 0.5, 'propthresh': 0.15,
              'toptwothresh': 0.15, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 5}
delegaterule['OK'] = {'state': 'Oklahoma', 'wta': 0.5, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 26, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['TN'] = {'state': 'Tennessee', 'wta': 0.667, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 9}
delegaterule['TN'] = {'state': 'Tennessee', 'wta': 0.667, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['TX'] = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 36}
delegaterule['TX'] = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
                 'toptwothresh': 0.2, 'numdelegates': 47, 'minthreshsplit': 2,
                 'allocbycd' : True}
# VA no CDs
delegatecdrule['VA'] = {'state': 'Virginia', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule["VA"] = {'state': 'Virginia', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 46, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['VT'] = {'state': 'Vermont', 'wta': 0.5, 'propthresh': 0.2, 'minthreshsplit': 1,
              'toptwothresh': 0.2, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['VT'] = {'state': 'Vermont', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 16, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['KS'] = {'state': 'Kansas', 'wta': 0.99, 'propthresh': 0.1, 'minthreshsplit': 1,
              'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 4}
delegaterule['KS'] = {'state': 'Kansas', 'wta': 0.5, 'propthresh': 0.10,
                 'toptwothresh': 0.99, 'numdelegates': 40, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['KY'] = {'state': 'Kentucky', 'wta': 0.99, 'propthresh': 0.05, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['KY'] = {'state': 'Kentucky', 'wta': 0.99, 'propthresh': 0.05,
                'toptwothresh': 0.99, 'numdelegates': 46, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['LA'] = {'state': 'Louisiana', 'wta': 0.99, 'propthresh': 0.01, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 6}
delegaterule['LA'] = {'state': 'Louisiana', 'wta': 0.99, 'propthresh': 0.05,
                'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                'allocbycd' : True}
delegatecdrule['ME'] = {'state': 'Maine', 'wta': 0.5, 'propthresh': 0.1, 'minthreshsplit': 1,
              'toptwothresh': 0.2, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['ME'] = {'state': 'Maine', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 23, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['PR'] = {'state': 'PuertoRico', 'wta': 0.5, 'propthresh': 0.1, 'minthreshsplit': 1,
              'toptwothresh': 0.2, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['PR'] = {'state': 'PuertoRico', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 23, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['HI'] = {'state': 'Hawaii', 'wta': 0.99, 'propthresh': 0.01, 'minthreshsplit': 1,
              'toptwothresh': 0.2, 'numdelegates': 3, 'numdistricts': 2}
delegaterule['HI'] = {'state': 'Hawaii', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['ID'] = {'state': 'Idaho', 'wta': 0.50, 'propthresh': 0.20, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['ID'] = {'state': 'Idaho', 'wta': 0.50, 'propthresh': 0.20,
                'toptwothresh': 0.99, 'numdelegates': 32, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['MI'] = {'state': 'Michigan', 'wta': 0.50, 'propthresh': 0.15, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['MI'] = {'state': 'Michigan', 'wta': 0.50, 'propthresh': 0.15,
                'toptwothresh': 0.99, 'numdelegates': 59, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['MN'] = {'state': 'Minnesota', 'wta': 0.85, 'propthresh': 0.10, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 8}
delegaterule['MN'] = {'state': 'Minnesota', 'wta': 0.85, 'propthresh': 0.1,
                'toptwothresh': 0.99, 'numdelegates': 14, 'minthreshsplit': 1,
                'allocbycd' : True}
delegatecdrule['WY'] = {'state': 'Wyoming', 'wta': 0.50, 'propthresh': 0.15, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 0, 'numdistricts': 0}
delegaterule['WY'] = {'state': 'Wyoming', 'wta': 0.50, 'propthresh': 0.15,
                'toptwothresh': 0.99, 'numdelegates': 59, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['MS'] = {'state': 'Mississippi', 'wta': 0.50, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 4}
delegaterule['MS'] = {'state': 'Mississippi', 'wta': 0.99, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['MO'] = {'state': 'Missouri', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 5, 'minthreshsplit': 1, 'numdistricts': 8}
delegaterule['MO'] = {'state': 'Missouri', 'wta': 0.01, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 12, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['FL'] = {'state': 'Florida', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule['FL'] = {'state': 'Florida', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 99, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['IL'] = {'state': 'Illinois', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 18}
delegaterule['IL'] = {'state': 'Illinois', 'wta': 0.01, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['NC'] = {'state': 'North Carolina', 'wta': 0.99, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule['NC'] = {'state': 'North Carolina', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 72, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['MP'] = {'state': 'Northern Marianas', 'wta': 0.99, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
delegaterule['MP'] = {'state': 'Northern Marianas', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 9, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['OH'] = {'state': 'Ohio'}
delegaterule['OH'] = {'state': 'Ohio', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 66, 'minthreshsplit': 1,
                 'allocbycd' : False}


#ignoring rules about if nobody gets 20%, assuming someone will get 20%
# if nobody gets 20%, then the rules are the same but set at 15%, then 10%.

#export delegaterule, delegatecdrule
