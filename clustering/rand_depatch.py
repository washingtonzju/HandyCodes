#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This code is used to depatch the large data into several smaller ones, so that we
can do the clustering with two levels.
"""

import sys
import re
import operator
import codecs
import math
import json
import random
import time


user_file = open("users_new.json", "r")
users = json.load(user_file)
user_file.close()
user_num= len(users)
seg_num = 100
segs = []
for i in range(0, seg_num):
    segs.append({})

random.seed(time.time())    
while len(users) > 0:
    for i in range(0, seg_num):
        if(len(users)<=0): break
        rand_idx = 0
        if(len(users)>1):
            rand_idx = random.randint(0, len(users)-1)
        #print rand_idx
        rand_user= users.keys()[rand_idx]
        segs[i][rand_user] = users[rand_user]
        del(users[rand_user])

for i in range(0, seg_num):
    print len(segs[i])
    seg_name = "part"+str(i)+".json"
    seg_file = open(seg_name, "w")
    seg_file.write(json.dumps(segs[i]))
    seg_file.close()
