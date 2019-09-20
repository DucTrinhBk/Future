import re
import sys
import statistic_words as st
import dbconnect as dc
def insert_new_keys(keys):
    for key in keys:
        print('thêm từ khóa "'+key+'"')
        print(bool(dc.execute(dc.defaultConnect(),"EXEC sp_DucTrinh_AddNewKeyword N'"+key+"'")[0]))
def get_list_keys(prefix):
    return list(map(lambda i: i['Name'].lower(),dc.get_list(dc.defaultConnect(),"EXEC sp_DucTrinh_GetAllKeys '"+prefix+"'")))
text = 'toi    muon    dat ban   vao sang mai cho 5 nguoi lon tai nha hang hai san bien dong'
text = text.strip()
text = re.sub(r'\s+',' ',text,flags=re.IGNORECASE)
p = 0
data = []
while(True):
    f = text[p:][0] 
    np = text[p:].find(' ')+1
    if np == 0:
        break
    item = dict()
    item['frlt'] = st.get_first_letter(text[p:][0])
    item['text'] = text[p:]
    keys = get_list_keys(item['frlt'])
    item['keys'] = dict()
    for key in keys:
        contain_quotient = st.contain_compare(text[p:],key)
        if contain_quotient > 0.95:
            item['keys'][key] = { 'key': key,'compare': contain_quotient}
    if len(item['keys']) > 0:
        data.append(item)
    p = p+np
print(data)
#insert_new_keys(['Nhà hàng Hải Sản Biển Đông'])