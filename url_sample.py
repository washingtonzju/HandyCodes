# -*- coding:utf8 -*-
import urllib2


def query_api_data(url, params):
    '''
    url is the path to the API like www.example.com/path/to/api
    params is a dictionary like {'param1':value, 'param2':value2, ... }
    This funciton return a tuple like (200, "returned contents")
    '''
    request = url + "?"
    for k,v in params.items():
        request = request + k + "=" + v

    resp_stream = urllib2.urlopen(request)

    status = resp_stream.readline().strip()

    stat_desc = resp_stream.readline().strip()

    if status[:-1] != "20":
        return status, stat_desc

    raw_data = resp_stream.readline()
    
    return status, raw_data
