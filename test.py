import re
import sys
import json
import statistic_words as st
import dbconnect as dc
from datetime import datetime as dt
from math import log
def insert_new_keys(keys):
    for key in keys:
        print('thêm từ khóa "'+key+'"')
        print(bool(dc.execute(dc.defaultConnect(),"EXEC sp_DucTrinh_AddNewKeyword N'"+key+"'")[0]))
def get_key(name):
    keys = dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetKeyByName N'"+name+"'")
    if len(keys) == 0:
        raise ValueError('không tìm thấy key')
    return keys[0]
def get_list_keys(prefix):
#    return list(map(lambda i: i['Name'].lower(),dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetAllKeys '"+prefix+"'")))
    return dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetAllKeys '"+prefix+"'")
#cập nhật hệ số huấn luyệun(alpha)
def training(text,k,threshold = None):
    if threshold is None:
        threshold= 0.9
    keys = dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetKeyByName N'"+k+"'")
    if len(keys) == 0:
        raise ValueError('Không tìm thấy key')
    key = keys[0]
    keyId = key['Id']
    keyName = key['Name'].lower()
    keyAlpha = float(key['Alpha'])
    score = st.compare_2_ways(text,keyName,keyAlpha)
    #tính độ lệch của alpha mới so với alpha cũ
    deltaAlpha = threshold ** (1/log(score,keyAlpha)) - keyAlpha
    return bool(dc.execute(dc.defaultConnect(),"EXEC sp_DucTrinh_UpdateAlphaById "+str(keyId)+","+str(keyAlpha+deltaAlpha*1.1))[0])
#lấy tất cả các key chứ text
def get_matches(text):
    text = text.strip()
    text = re.sub(r'\s+',' ',text,flags=re.IGNORECASE)
    #Lưu lại vị trí của từ hiện tại
    p = 0
    data = []
    keys = get_list_keys(st.get_first_letter(text))
    '''
    for key in keys:
        score = st.contain_compare(key,text)
        if score >= 0.9:
            data.append({'key': key,'score' : score})
    print(json.dumps(data,ensure_ascii=False))
    '''
    start = dt.now()
    print(json.dumps(st.get_all_keys(text,0.9,get_list_keys("*")),ensure_ascii=False))
    print("time: "+str((dt.now() - start).total_seconds() * 1000)+" mili giây")
'''
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
        #kiểm tra xem key có nằm trong text không
        score = st.contain_compare(text[p:],key)
        if score >= 0.8:
            item['keys'][key] = { 'key': key,'compare': score}
    if len(item['keys']) > 0:
        data.append(item)
    np = text[p:].find(' ')+1
    #nếu không còn từ nào nữa thì thoát vòng lặp
    if np == 0:
        break
    #Nhảy đến từ tiếp theo
    p = p+np
start = dt.now()
print(json.dumps(data,ensure_ascii=False))
print("time: "+str((dt.now() - start).total_seconds() * 1000)+" mili giây")
print("")
start = dt.now()
print(json.dumps(st.get_all_keys(text,0.95,get_list_keys("*")),ensure_ascii=False))
print("time: "+str((dt.now() - start).total_seconds()* 1000)+" mili giây")
'''
# print('')
#print(get_list_keys('*'))
#print(st.get_all_keys(text,0.8,get_list_keys('*')))
#insert_new_keys(open("body.txt", "r", encoding="utf8").read().split('\n'))