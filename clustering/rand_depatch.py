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
import heapq
import elbowcriterion
from CosineLib import CosineLib

class Agglomerative:
    def __init__(self, data, vectors=None, from_bottom=True):
        
        self.index = 0
        self.clusters = {}
        self.vectors = {}
        self.from_bottom = from_bottom
        if from_bottom == True:
            for key, vect in data.items():
                self.clusters[self.index] = [key]
                self.index += 1
            self.vectors = data
        else:
            self.clusters = data
            next_idx = 0
            for key in data.keys():
                key = int(key)
                if key > next_idx:
                    next_idx = key
            self.index = next_idx + 1
            self.vectors = vectors
        self.heaps = {}

    def cluster_distance(self, idxa, idxb):
        dis = 0.0
        sz_a = len(self.clusters[idxa])
        sz_b = len(self.clusters[idxb])
        if sz_a > sz_b:
            for i in range(0, sz_b):
                dis += self.dis_mat[(self.clusters[idxb][i], idxa)]
        else:
            for i in range(0, sz_a):
                dis += self.dis_mat[(self.clusters[idxa][i], idxb)]
        dis /= sz_a * sz_b
        #print idxa, idxb, dis
        return dis
    
    def prepare(self):
        self.heaps = {}
        for key in self.clusters.keys():
            self.heaps[key] = []

        # dis_mat should be the distance from points to clusters
        self.dis_mat = {}
        ls = self.vectors.keys()
        cs = self.clusters.keys()
        start_time = time.time()
        cnt = 0
        for i in range(0, len(cs)):
            lst_1 = self.clusters[i]
            for j in range(i+1, len(cs)):
                cnt += 1
                """
                if cnt % 100 == 0:
                    print "calculate the", cnt, "and cost", time.time() - start_time
                """
                dis = 0.0
                lst_2 = self.clusters[j]
                for v1 in lst_1:
                    for v2 in lst_2:
                        dis += 1.0 - CosineLib.jaccard_score(self.vectors[v1], self.vectors[v2])
                dis /= len(lst_1)
                dis /= len(lst_2)
                self.dis_mat[(cs[i], cs[j])] = dis
                self.dis_mat[(cs[j], cs[i])] = dis
                        
        print "dis_mat cost: ", (time.time() - start_time)/60.0, " mins"
        start_time = time.time()
        ks = self.clusters.keys()        
        for i in range(0, len(ks)):
            for j in range(i+1, len(ks)):
                ia = ks[i]
                ib = ks[j]
                dis = self.dis_mat[(ia, ib)]
                heapq.heappush(self.heaps[ia], (dis, ib))
                heapq.heappush(self.heaps[ib], (dis, ia))
        print "heap building cost: ", (time.time() - start_time)/60.0, " mins"
    
    def iterating(self, thresh_hold = None, file_prefix = None):
        start_time = time.time()
        curr_time = time.time()
        scores = []
        while True:
            old_time = curr_time
            #print "Cluster Size: " + str(len(self.clusters))
            
            min_val = 1000000000000
            min_a = 0
            min_b = 0
            for key, heap in self.heaps.items():
                while True:
                    if heap[0][1] in self.clusters.keys():
                        break
                    else:
                        heapq.heappop(heap)
                if heap[0][0] < min_val:
                    min_val = heap[0][0]
                    min_a = key
                    min_b = heap[0][1]
            new_id = self.index;
            self.index += 1

            new_lst = self.clusters[min_a] + self.clusters[min_b]
            
            
            # add new clusters element
            self.clusters[new_id] = new_lst
            # add new heaps element
            self.heaps[new_id] = []
            ls = self.vectors.keys()
            # update dis_mat
            for idx in self.clusters.keys():
                if idx == min_a or idx == min_b or idx == new_id:
                    continue
                dis = 0.0
                dis += self.dis_mat[(idx, min_a)]*len(self.clusters[min_a])
                dis += self.dis_mat[(idx, min_b)]*len(self.clusters[min_b])
                dis /= (len(self.clusters[min_a]) + len(self.clusters[min_b]))
                self.dis_mat[(idx, new_id)] = dis
                self.dis_mat[(new_id, idx)] = dis
                heapq.heappush(self.heaps[new_id], (dis, idx))
                heapq.heappush(self.heaps[idx], (dis, new_id))
                del(self.dis_mat[(idx, min_a)])
                del(self.dis_mat[(idx, min_b)])
                del(self.dis_mat[(min_a, idx)])
                del(self.dis_mat[(min_b, idx)])
                
            # delete cluster, heaps    
            del(self.clusters[min_a])
            del(self.clusters[min_b])
            del(self.heaps[min_a])
            del(self.heaps[min_b])

            if file_prefix != None:
                file_name = file_prefix+"_res_"+ str(len(self.clusters))+".json"
            else:
                file_name = "result"+str(len(self.clusters))+".json"
                
            if self.from_bottom == True and thresh_hold != None:
                if min_val >= thresh_hold:                    
                    json_file = open(file_name, "w")
                    json_file.write(json.dumps(self.clusters))
                    json_file.close()
                    break            
            elif len(self.clusters) < 51 and thresh_hold == None:
                json_file = open(file_name, "w")
                json_file.write(json.dumps(self.clusters))
                json_file.close()
                print "min_dis:", min_val, "number of clusters:", len(self.clusters), "cost time:", (curr_time - old_time), "secs"
                scores.append(min_val)
                
            else:
                print "min_dis:", min_val, "number of clusters:", len(self.clusters), "cost time:", (curr_time - old_time), "secs"
            if len(self.clusters) < 2:
                break
        if thresh_hold == None:
            scores.reverse()
            idx, max_var = elbowcriterion.find_best_points(scores)
            print "Best result is : ", idx, " and the max derivative variances is : ", max_var
        print "Cost ", (curr_time - start_time)/60.0, "mins"
        
if __name__ == "__main__":

    user_file = open("users_new.json", "r")
    users = json.load(user_file)
    sample_users = {}
    cnt_s = 0
    for key, val in users.items():
        sample_users[key] = val
        cnt_s = cnt_s + 1
        if cnt_s > 2000:
            break
        
    user_file.close()
    agg = Agglomerative(sample_users)
    print len(agg.clusters)
    print "preparing"
    agg.prepare()
    print "iterating"
    agg.iterating()
    """
    cnt = 0
    for key, val in agg.heaps.items():
        cnt += 1
        if cnt > 10:
            break
        print key, val
    """
