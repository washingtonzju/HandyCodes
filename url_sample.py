# -*- coding:utf8 -*-
import urllib2


def query_api_data(url, params):

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
