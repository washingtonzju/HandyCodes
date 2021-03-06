import json
import codesc

def gen_titles(data, f_name, user_name):
    '''
    codecs is a class that solve character issues.
    codecs.open() is a method that replace open(). It provides character supports.
    '''
    data_lst = json.loads(data.decode("utf-8-sig"))

    csv_file = codecs.open(f_name, "w", encoding="utf-8")
    titles = [u"username"]
    #print data_lst
    titles.extend(data_lst[0].keys())
    
    csv_file.write((u",".join(titles))+"\n")
    csv_file.close()
