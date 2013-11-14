def parsing_log(data, f_name, user_name):
    data_lst = json.loads(data.decode("utf-8-sig"))
    csv_file = codecs.open(f_name, "a+", encoding="utf-8")
    for log in data_lst:
        row = [unicode(user_name)]
        for k, v in log.items():
            print k, v
            row.append(unicode(v))
        #print (u",".join(row))
        csv_file.write((u",".join(row))+"\n")
    csv_file.close()
