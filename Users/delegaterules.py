#!/usr/bin/python
import sys
# rules for Texas
# wta level 50%, prop thresh is 20%
# Tx district rules: 36 districts x 3 delegates.
# top > .5:  3 to top; top > .2 and < .5: 2 to top, 1 to 2nd
# top < .2: 1 each to top 3
# Definitions:
# wta = winner-take-all level for district or state. A winner-take-all state has wta=0.01
# wtathresh = if only one candidate is above that level, they are winner-take-all winner-take-all
# propthesh = proportional threshold
# wta thresh - one candidate gets above that 0.2 and nobody else does = 0.2

#ignoring rules about if nobody gets 20%, assuming someone will get 20%
# if nobody gets 20%, then the rules are the same but set at 15%, then 10%.


no_cds = {}
delegaterule={}
delegatecdrule={}
# Alabama Primary (50 total delegates/47 bound) - Proportional with 20% threshold
delegaterule['AL'] = {'state': 'Alabama', 'wta': 0.5, 'wtathresh': 0.2,
                 'propthresh': 0.2, 'toptwothresh': 0.2, 'numdelegates': 26, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['AL'] = {'wta': 0.5, 'propthresh': 0.2, 'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 7}
# Alaska Caucuses (28/25) Proportional with 13% threshold
delegaterule['AK'] = {'state': 'Alaska', 'wta': 0.99, 'propthresh': 0.13,
                 'toptwothresh': 0.99, 'numdelegates': 25, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['AK'] = {'state': 'Alaska', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
# Arkansas Primary (40/37) - Proportional with 15% threshold
delegaterule['AR'] = {'state': 'Arkansas', 'wta': 0.99, 'propthresh': 0.15,
                 'toptwothresh': 0.2, 'numdelegates': 25, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['AR'] = {'state': 'Arkansas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 4}
# Georgia Primary (76) - Proportional with 20% threshold
# divide 31 proportionally and give a 3 del bonus to the top vote-getter
delegaterule['GA'] = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.2, 'topvotedelbonus': 3,
                      'toptwothresh': 0.2, 'numdelegates': 34, 'minthreshsplit': 2,
                      'allocbycd' : True}
delegatecdrule['GA'] = {'state': 'Georgia', 'wta': 0.5, 'propthresh': 0.01,
              'toptwothresh': 0.01, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 14}
# Massachusetts Primary (42/39) - Proportional with 5% threshold
delegaterule['MA'] = {'state': 'Massachusetts', 'wta': 0.99, 'propthresh': 0.05,
                 'toptwothresh': 0.05, 'numdelegates': 39, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['MA'] = {'state': 'Massachusetts', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 0, 'minthreshsplit': 2, 'numdistricts': 0}
# Oklahoma Primary (43/40) Proportional with 15% threshold
delegaterule['OK'] = {'state': 'Oklahoma', 'wta': 0.5, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 26, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['OK'] = {'state': 'Oklahoma', 'wta': 0.5, 'propthresh': 0.15,
              'toptwothresh': 0.15, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 5}
# Tennessee Primary (58/55) Proportional with 20% threshold
delegaterule['TN'] = {'state': 'Tennessee', 'wta': 0.667, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['TN'] = {'state': 'Tennessee', 'wta': 0.667, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 9}
# Texas Primary (155/152) Proportional with 20% threshold
delegaterule['TX'] = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
                 'toptwothresh': 0.2, 'numdelegates': 47, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['TX'] = {'state': 'Texas', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 36}
# Vermont Primary (16/13)Proportional with 20% threshold (lowerthresholds ignored)
delegaterule['VT'] = {'state': 'Vermont', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 16, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['VT'] = {'state': 'Vermont'}
# Virginia Primary (49/46) Proportional - no CDs
delegaterule["VA"] = {'state': 'Virginia', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 46, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['VA'] = {'state': 'Virginia'}
# Minnesota Caucuses (38/35) - Proportional with 10% threshold
delegaterule['MN'] = {'state': 'Minnesota', 'wta': 0.85, 'propthresh': 0.1,
                'toptwothresh': 0.99, 'numdelegates': 14, 'minthreshsplit': 1,
                'allocbycd' : True}
delegatecdrule['MN'] = {'state': 'Minnesota', 'wta': 0.85, 'propthresh': 0.10, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 8}
# Wyoming Caucuses (29/0), North Dakota Caucuses(28/0)  No presidential preference poll, all delegates are officially unbound.
delegaterule['WY'] = {'state': 'Wyoming', 'wta': 0.50, 'propthresh': 0.15,
                'toptwothresh': 0.99, 'numdelegates': 59, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['WY'] = {'state': 'Wyoming'}

#    Kansas Caucuses (40)  Proportional with 10% threshold
delegaterule['KS'] = {'state': 'Kansas', 'wta': 0.5, 'propthresh': 0.10,
                 'toptwothresh': 0.99, 'numdelegates': 40, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['KS'] = {'state': 'Kansas', 'wta': 0.99, 'propthresh': 0.1, 'minthreshsplit': 1,
              'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 4}
#    Kentucky Caucuses (45/42)  Proportional with 5% threshold
delegaterule['KY'] = {'state': 'Kentucky', 'wta': 0.99, 'propthresh': 0.05,
                'toptwothresh': 0.99, 'numdelegates': 46, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['KY'] = {'state': 'Kentucky'}
#    Louisiana Primary (46/43) Proportional with 20% threshold statewide, no threshold for congressional district delegates
delegaterule['LA'] = {'state': 'Louisiana', 'wta': 0.99, 'propthresh': 0.05,
                'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                'allocbycd' : True}
delegatecdrule['LA'] = {'state': 'Louisiana', 'wta': 0.99, 'propthresh': 0.01, 'minthreshsplit': 1,
                'toptwothresh': 0.99, 'numdelegates': 3, 'numdistricts': 6}
#    Maine Caucuses (23/20)  Proportional with 10% threshold
delegaterule['ME'] = {'state': 'Maine', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 23, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['ME'] = {'state': 'Maine'}
#    Puerto Rico Primary (23)  Proportional with 20% threshold
delegaterule['PR'] = {'state': 'PuertoRico', 'wta': 0.5, 'propthresh': 0.20,
                 'toptwothresh': 0.2, 'numdelegates': 23, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['PR'] = {'state': 'PuertoRico'}

#    Hawaii Caucuses (19/16)  Proportional - rounding
delegaterule['HI'] = {'state': 'Hawaii', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['HI'] = {'state': 'Hawaii', 'wta': 0.99, 'propthresh': 0.01, 'minthreshsplit': 1,
              'toptwothresh': 0.2, 'numdelegates': 3, 'numdistricts': 2}
#    Idaho Primary (32) Proportional with 20% threshold
delegaterule['ID'] = {'state': 'Idaho', 'wta': 0.50, 'propthresh': 0.20,
                'toptwothresh': 0.99, 'numdelegates': 32, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['ID'] = {'state': 'Idaho'}
#    Michigan Primary (59/56) Proportional with 15% threshold - rounding up/down
delegaterule['MI'] = {'state': 'Michigan', 'wta': 0.50, 'propthresh': 0.15,
                'toptwothresh': 0.99, 'numdelegates': 59, 'minthreshsplit': 1,
                'allocbycd' : False}
delegatecdrule['MI'] = {'state': 'Michigan'}
#    Mississippi Primary (40/36) Proportional with 15% threshold
delegaterule['MS'] = {'state': 'Mississippi', 'wta': 0.99, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 28, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['MS'] = {'state': 'Mississippi', 'wta': 0.50, 'propthresh': 0.15,
              'toptwothresh': 0.15, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 4}

#     District of Columbia Convention (19) Proportional with 15% threshold
delegaterule['DC'] = {'state': 'District of Columbia', 'wta': 0.5, 'propthresh': 0.15,
                 'toptwothresh': 0.2, 'numdelegates': 19, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['DC'] = {'state': 'District of Columbia'}

#    Missouri Primary (52/49)  Winner take all above 50%, otherwise winter take all by congressional district
delegaterule['MO'] = {'state': 'Missouri', 'wta': 0.01, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 12, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['MO'] = {'state': 'Missouri', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 5, 'minthreshsplit': 1, 'numdistricts': 8}
#    Florida Primary (99)  Winner take all
delegaterule['FL'] = {'state': 'Florida', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 99, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['FL'] = {'state': 'Florida'}
#    Illinois Primary (69)  Statewide delegates WTA,  CD delegates elected directly on ballot and bound as they declare
delegaterule['IL'] = {'state': 'Illinois', 'wta': 0.01, 'wtathresh': 0.50,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['IL'] = {'state': 'Illinois', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 18}
#    North Carolina Primary (72/69)  Proportional
delegaterule['NC'] = {'state': 'North Carolina', 'wta': 0.99, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 72, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['NC'] = {'state': 'North Carolina'}
#    Northern Mariana Islands Caucuses (9) Winner take all
delegaterule['MP'] = {'state': 'Northern Marianas', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 9, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['MP'] = {'state': 'Northern Marianas'}
#    Ohio Primary (66) Winner take all
delegaterule['OH'] = {'state': 'Ohio', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 66, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['OH'] = {'state': 'Ohio'}
# March 19, 2016 (9 bound delegates)
#    U.S. Virgin Islands (9) Winner take all
delegaterule['VI'] = {'state': 'US Virgin Islands', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 9, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['VI'] = {'state': 'US Virgin Islands'}
#March 22, 2016 (107 bound delegates)
#    American Samoa Convention (9) Delegates elected and bound at convention
delegaterule['AS'] = {'state': 'American Samoa', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.99, 'numdelegates': 6, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['AS'] = {'state': 'American Samoa'}
#    Arizona Primary (58) Winner take all
delegaterule['AZ'] = {'state': 'Arizona', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 58, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['AZ'] = {'state': 'Arizona'}
#    Utah Caucuses (40)Proportional with 15% threshold
delegaterule['UT'] = {'state': 'Utah', 'wta': 0.50, 'propthresh': 0.15,
                 'toptwothresh': 0.15, 'numdelegates': 40, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['UT'] = {'state': 'Utah'}

# April 5, 2016 (42 bound)
# Wisconsin Primary (42) Winner take all statewide and by congressional district
delegaterule['WI'] = {'state': 'Wisconsin', 'wta': 0.01,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 18, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['WI'] = {'state': 'Wisconsin', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 8}
# April 9, 2016 - Colorado Convention (37/0) Delegates elected at district and state conventions, and bound as they declare

# April 19, 2016 - New York Primary (95/92) Proportional with 20% threshold
delegaterule['NY'] = {'state': 'New York', 'wta': 0.5,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 14, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['NY'] = {'state': 'New York', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 27}
# Northeast Primary: April 26, 2016 (109 bound)
# Connecticut Primary (28/25) Winner take all above 50%, otherwise proportional with 20% threshold statewide, winner take all by congressional district
delegaterule['CT'] = {'state': 'Connecticut', 'wta': 0.5,
                 'propthresh': 0.15, 'toptwothresh': 0.99, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['CT'] = {'state': 'Connecticut', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 5}
# Delaware Primary (16) Winner take all
delegaterule['DE'] = {'state': 'Delaware', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 16, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['DE'] = {'state': 'Delaware'}
# Maryland Primary (38)  WTA
delegaterule['MD'] = {'state': 'Maryland', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 14, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['MD'] = {'state': 'Maryland', 'wta': 0.01, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 8}
# Pennsylvania Primary (71/14) WTA statewide, remaining delegates elected on ballot and unbound
delegaterule['PA'] = {'state': 'Pennsylvania', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 17, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['PA'] = {'state': 'Pennsylvania', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 18}
# Rhode Island Primary (19/16) Proportional with 10% threshold
# CD rules are a 1-1-1 split in a 3-way race. alloc_split not used in CDs.
delegaterule['RI'] = {'state': 'Rhode Island', 'wta': 0.99,
                 'propthresh': 0.1, 'toptwothresh': 0.1, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['RI'] = {'state': 'Rhode Island', 'wta': 0.5, 'propthresh': 0.1,
              'toptwothresh': 0.9, 'numdelegates': 3, 'minthreshsplit': 3, 'numdistricts': 2}
# May 3, 2016 - Indiana Primary (57/54) Winner take all statewide and by congressional district
delegaterule['IN'] = {'state': 'Indiana', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 30, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['IN'] = {'state': 'Indiana', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 9}
# May 10, 2016 (67 bound)
# Nebraska Primary (36) Winner take all
delegaterule['NE'] = {'state': 'Nebraska', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 36, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['NE'] = {'state': 'Nebraska'}
# West Virginia Primary (34/31) Delegates elected directly on ballot and bound by preference (like WTA)
delegaterule['WV'] = {'state': 'West Virginia', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 22, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['WV'] = {'state': 'West Virginia', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 3}
# May 17, 2016 (25 bound)
# Oregon Primary (28/25) Proportional
delegaterule['OR'] = {'state': 'Oregon', 'wta': 0.99,
                 'propthresh': 0.04, 'toptwothresh': 0.04, 'numdelegates': 28, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['OR'] = {'state': 'Oregon'}
# May 27, 2016 (41 bound)
# Washington Primary (44/41) Proportional with 20% threshold. CD rules are 3-way split if 3 above 20%
delegaterule['WA'] = {'state': 'Washington', 'wta': 0.99, 'propthresh': 0.2,
                 'toptwothresh': 0.2, 'numdelegates': 14, 'minthreshsplit': 2,
                 'allocbycd' : True}
delegatecdrule['WA'] = {'state': 'Washington', 'wta': 0.5, 'propthresh': 0.2,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 2, 'numdistricts': 10}
# Last Call: June 7, 2016 (294 bound)
# California Primary (172/169) Winner take all statewide and by congressional district
delegaterule['CA'] = {'state': 'California', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 13, 'minthreshsplit': 1,
                 'allocbycd' : True}
delegatecdrule['CA'] = {'state': 'California', 'wta': 0.01, 'propthresh': 0.01,
              'toptwothresh': 0.2, 'numdelegates': 3, 'minthreshsplit': 1, 'numdistricts': 53}
# Montana Primary (27) Winner take all
delegaterule['NE'] = {'state': 'Nebraska', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 36, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['NE'] = {'state': 'Nebraska'}

# New Jersey Primary (51) Winner take all
delegaterule['NJ'] = {'state': 'New Jersey', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 51, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['NJ'] = {'state': 'New Jersey'}
# New Mexico Primary (24/21) Proportional with 15% threshold
delegaterule['NM'] = {'state': 'New Mexico', 'wta': 0.99,
                 'propthresh': 0.15, 'toptwothresh': 0.15, 'numdelegates': 24, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['NM'] = {'state': 'New Mexico'}
# South Dakota Primary (29/26) Winner take all
delegaterule['SD'] = {'state': 'South Dakota', 'wta': 0.01, 'propthresh': 0.01,
                 'toptwothresh': 0.2, 'numdelegates': 29, 'minthreshsplit': 1,
                 'allocbycd' : False}
delegatecdrule['SD'] = {'state': 'South Dakota'}
