#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import operator
import codecs
import math
import json

class CosineLib:
    def __init__(self):
        pass

    @staticmethod
    def jaccard_score(uvector, tvector):
        cnt = 0.0
        for idx in uvector.keys():
            if idx in tvector.keys():
                cnt += 1
        return cnt/(len(uvector) + len(tvector) - cnt)
        
    @staticmethod
    def cosine_score(uvector, tvector):
        """
        Calculate the cosine similarity. input vector params: {1:0.4, 2:054, 3:1.3, ... }
        The vector is sparse vector
        """
        first_part=0.0
        for idx, val in uvector.items():
            if idx not in tvector.keys():
                continue
            first_part = first_part + val*tvector[idx]
        u_sz = 0.0
        for idx, val in uvector.items():
            u_sz = u_sz + val * val
        u_sz = math.sqrt(u_sz)

        t_sz = 0.0
        for idx, val in tvector.items():
            #print "val is: ",
            #print val
            t_sz = t_sz + val * val
        t_sz = math.sqrt(t_sz)

        if t_sz == 0.0 or u_sz == 0.0:
            return 0.0
        else:
            return first_part/(u_sz * t_sz)

    @staticmethod    
    def merge_vector(base_vector, operand_vector):
        for idx, value in operand_vector.items():
            if idx in base_vector.keys():
                base_vector[idx] = base_vector[idx] + value
            else:
                base_vector[idx] = value    
        
    @staticmethod
    def load_data(data_file_list):
        """
        """
        vectors = {}
        for jfile in data_file_list:
            vector_file = open(jfile, "r")
            vector_seg = json.load(vector_file)[0]
            vectors.update(vector_seg)
            vector_file.close()
        return vectors

    @staticmethod
    def save_data(data_file_name, data):
        """
        """
        data_file = open(data_file_name, "w")
        data_file.write(json.dumps([data]))
        data_file.close()
