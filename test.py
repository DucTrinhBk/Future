import re
import sys
import json
import statistic_words as st
import dbconnect as dc
from datetime import datetime as dt
def insert_new_keys(keys):
    for key in keys:
        print('thêm từ khóa "'+key+'"')
        print(bool(dc.execute(dc.defaultConnect(),"EXEC sp_DucTrinh_AddNewKeyword N'"+key+"'")[0]))
def get_list_keys(prefix):
    return list(map(lambda i: i['Name'].lower(),dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetAllKeys '"+prefix+"'")))
text = 'hello' if len(sys.argv) < 2 else sys.argv[1]
text = text.strip()
text = re.sub(r'\s+',' ',text,flags=re.IGNORECASE)
p = 0
data = []
while(True):
    f = text[p:][0] 
    item = dict()
    item['frlt'] = st.get_first_letter(text[p:][0])
    item['text'] = text[p:]
    keys = get_list_keys(item['frlt'])
    item['keys'] = dict()
    for key in keys:
        contain_quotient = st.contain_compare(text[p:],key)
        if contain_quotient >= 0.95:
            item['keys'][key] = { 'key': key,'compare': contain_quotient}
    if len(item['keys']) > 0:
        data.append(item)
    np = text[p:].find(' ')+1
    if np == 0:
        break
    p = p+np
start = dt.now()
print(json.dumps(data,ensure_ascii=False))
print("time: "+str((dt.now() - start).total_seconds() * 1000)+" mili giây")
print("")
start = dt.now()
print(json.dumps(st.get_all_keys(text,0.95,get_list_keys("*")),ensure_ascii=False))
print("time: "+str((dt.now() - start).total_seconds()* 1000)+" mili giây")
# print('')
#print(get_list_keys('*'))
#print(st.get_all_keys(text,0.8,get_list_keys('*')))
#insert_new_keys(open("body.txt", "r", encoding="utf8").read().split('\n'))