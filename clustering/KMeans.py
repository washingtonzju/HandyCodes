#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import operator
import codecs
import math
import random
import json
import time
from CosineLib import CosineLib

class KMeans:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.seeds = []
        self.min = 0.000001
                
    def generate_seeds(self, seeds_number):
        self.seeds = []
        tmp_dict = {}
        for cnt in range(0, seeds_number):
            rand_idx  = random.randint(0, self.size-1)            
            while rand_idx in tmp_dict.keys():
                rand_idx  = random.randint(0, self.size-1)

            #print rand_idx
            self.seeds.append(self.data.items()[rand_idx][0])
            tmp_dict[rand_idx] = 1           

    def run(self):        
        cnt = 0
        while True:
            s_time = time.time()
            cluster = {}
            # vectors to its cluster 
            for id, vector in self.data.items():
                c_id = self.seeds[0]
                min_dis = 1.0/self.min
                tmp_dis = 0.0
                for seed in self.seeds:
                    tmp_dis = CosineLib.cosine_score(vector, self.data[seed])
                    if abs(tmp_dis) < self.min:
                        tmp_dis = 1.0/self.min
                    else:
                        tmp_dis = 1.0/tmp_dis
                    tmp_dis = math.log(tmp_dis, 2)
                    if tmp_dis < min_dis:
                        c_id = seed
                        min_dis = tmp_dis
                if c_id not in cluster.keys():
                    cluster[c_id] = [id]
                else:
                    cluster[c_id].append(id)
            e_time = time.time()
            print "cost " + str(e_time - s_time)
            #for seed in self.seeds:
            #    print len(cluster[seed])

            # adjust the center
            o2n = {}
            for center, pnts in cluster.items():
                print len(pnts)
                midd = {}
                for pnt in pnts:
                    pvector = self.data[pnt]
                    CosineLib.merge_vector(midd, pvector)

                c_id = center
                min_dis = 1.0/self.min
                tmp_dis = 0.0
                
                for pnt in pnts:
                    tmp_dis = CosineLib.cosine_score(self.data[pnt], midd)
                    # print "tmp_dis: " + str(tmp_dis)
                    if abs(tmp_dis) < self.min:
                        tmp_dis = 1.0/self.min
                    else:
                        tmp_dis = 1.0/tmp_dis
                    tmp_dis = math.log(tmp_dis, 2)
                    if tmp_dis < min_dis:
                        c_id = pnt
                        min_dis = tmp_dis
                o2n[center] = c_id
                                
            e2_time = time.time()

            print "adjust cost " + str(e2_time - e_time)
                            
            cnt = cnt + 1
            if cnt > 40:
                break
            
            flag = False
            for key, val in o2n.items():
                if key != val:
                    flag = True
                    break
            if flag == False:
                break
            self.seeds = []
            for key, val in o2n.items():
                self.seeds.append(val)
        return cluster
