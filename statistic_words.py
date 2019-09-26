import re,json
from datetime import datetime as dt
from unidecode import unidecode
vowels = ['a','e','i','o','u','y']
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True
#len,num_of_syll,vls,first_letter
def u(word):
    if is_number(word):
        return '@num'
    return unidecode(word)
def get_num_of_sylables(sens):
    sens = sens.lower()
    if sens.strip() == '':
        return 0
    ws = sens.split()
    if(len(ws) > 1):
        return sum([get_num_of_sylables(w) for w in ws])
    if not sens.isalpha():
        return 1
    if is_number(sens):
        return 1
    i = 0
    l1 = ''
    s1 = u(sens).lower()
    for l in s1:
        if (l in vowels and l1 not in vowels ):
            i+=1
        l1 = l    
    return max(i,1)
def get_first_letter(phrase):
    phrase = phrase.lower().strip()
    if phrase == '':
        return '\0'
    words = phrase.split()
    if len(words) == 1:
        if not words[0].isalpha():
            return '@'
        return words[0][0]
    f = ''
    for word in words:
        f+=get_first_letter(word)
    return f
def get_vowels(phrase):
    phrase = phrase.lower().strip()
    if phrase == '':
        return []
    words = phrase.split()
    vls = []
    if len(words) == 1:
        if not words[0].isalpha():
            return words
        vl = ''
        w = words[0] + ' '
        for l in w:
            if (u(l) in vowels):
                vl+=l
            else:
                if vl is not '':
                    vls.append(vl)
                vl = ''
        return vls if len(vls) > 0 else ['']
    for word in words:
        vls+=get_vowels(word)
    return vls

def is_word(w):
    if is_number(w):
        return True
    for l in w:
        if not l.isalpha():
            return False
    return True
def get_w_pos_in_sen(w):
    i = 0
    r = ""
    len_ = len(w)
    while((not w[i].isalpha()) and (not w[i].isdigit())):
        if i == len_ - 1:
            break
        i+=1
    for l in w:
        if l.isalpha() or l.isdigit():
            r += l
    if r == "":
        return "End",""
    if i == 0:
        if is_word(w):
            return "Between",r.lower()
        else:
            return "End",r.lower()
    return "Begin",r.lower()
def compare_2_ways(w1,w2):
    return (compare(w1,w2) + compare(w2,w1))/2
#buffet buftef
'''
[
    0.99 # 'len_ch',
    0.9  # 'num_of_syll',
    0.99 # 'first_letter_utf8',
    0.8  # 'first_letter_ascii',
    0.99 # 'vowels_utf8',
    0.9  # 'vowels_ascii',
    0.99 # 'hierachy_utf8',
    0.9  # 'hierachy_ascii'
]
#độ mạnh của từ khóa
'''
def compare(w1,w2):
    w1,w2 = [re.sub(r'\s+',' ',w1.lower().strip()),re.sub(r'\s+',' ',w2.lower().strip())]
    if w1.replace(' ','') == w2.replace(' ',''):
        return 1
    i1 = len(w1),get_num_of_sylables(w1),get_first_letter(w1),get_vowels(w1)
    i2 = len(w2),get_num_of_sylables(w2),get_first_letter(w2),get_vowels(w2),list(map(lambda item : u(item),i1[3]))
    d = 0.99**abs(i1[0] - i2[0]) * 0.9**abs(i1[1]-i2[1]) * 0.99**int(not i1[2] == i2[2])*0.9**int(not u(i1[2]) in u(i2[2]))
    for fl in i1[2]:
        d*0.9**int(not u(fl) in u(i2[2]))
    for vl in i1[3]:
        d*=(0.99**int(vl not in i2[3]) * 0.9**int(u(vl) not in i2[4]))
    #check thu tu cac chu cai co khop nhau hay khong
    letters = dict()
    map_pos = -1
    w1 = w1.replace(" ","")
    w2 = w2.replace(" ","")
    for l in w1:
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(w2,l,letters[l])
        d*=(0.99**int(m<=map_pos))
        map_pos = m
    letters = dict()
    map_pos = -1
    for l in u(w1):
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(u(w2),l,letters[l])
        d*=(0.9**int(m<=map_pos))
        map_pos = m
    return d**(1/min(i1[1],i2[1]))
#if w1 contain w2
def contain_compare(w1,w2):
    w1,w2 = [re.sub(r'\s+',' ',w1.lower().strip()),re.sub(r'\s+',' ',w2.lower().strip())]
    w1 = w1.replace(" ","")
    w2 = w2.replace(" ","")
    d = 1
    map_pos = -1
    letters = dict()
    for l in w2:
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(w1,l,letters[l])
        d*=(0.99**int(m<=map_pos))
        map_pos = m
    letters = dict()
    map_pos = -1
    for l in u(w2):
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(u(w1),l,letters[l])
        d*=(0.9**int(m<=map_pos))
        map_pos = m
    return d**(1/get_num_of_sylables(w2))
#tìm vị trí thứ @pos của @_sub trong chuỗi @_str
def find_sub_str_with_pos(_str,_sub,pos):
    if(pos <= 0):
        return -1
    p = _str.find(_sub)
    for i in range(1,pos):
        m = _str[p+1:].find(_sub)
        if(m == -1):
            return - 1
        p+=(m+1)
    return p

def get_words():
    f = open("words.txt", "r")
    return json.loads(f.read())
def len_sen(sen):
    ws = sen.strip().split()
    return len(ws)
def get_word_by_pos(sen,pos):
    n = len_sen(sen)
    if pos >= n:
        pos%n
    i = 0
    ws = sen.split()
    for w in ws:
        if i == pos:
            return w
        i+=1
    return ''
def get_all_keys(sen,match,keys):
    if match <0 or match > 1:
        print("match must be from 1 to zero")
        return []
    results = []
    keys = sorted(keys,key=len,reverse=True)
    ws = sen.lower().split()
    i = 0
    n = len(ws)
    while(i < n):
        if not ws[i].isalpha():
            results.append([('_notalpha_'+ws[i]+'_'+str(i)+'_'+str(len(ws[i])),i,i+1,1)])
            i+=1
            continue
        temps = []
        for key in keys:
            if u(key[0]) == u(ws[i][0]) : 
                rs = ()
                if len_sen(key) == 1:
                    f = compare_2_ways(ws[i],get_word_by_pos(key,0))
                    if f > match:
                        rs = (key,i,i+1,compare_2_ways(ws[i],get_word_by_pos(key,0)))
                else:
                    j = 0
                    sub_sen = ''
                    len_key = len_sen(key)
                    while(i+j < n):
                        sub_sen+=(ws[i+j]+" ")
                        cp = compare_2_ways(sub_sen,key)
                        if j > len_key +2:
                            break
                        if cp > match:
                            if len(rs) ==0:
                                    rs = (key,i,i+j+1,cp)
                            else:
                                if rs[3] < cp or (rs[3] == cp and (i+j+1) > rs[2]):
                                    rs = (key,i,i+j+1,cp)
                        j += 1
                if len(rs) > 0:
                    temps.append(rs)
                    if rs[2] > n:
                        break
        if len(temps) > 0:
            results.append(temps)
        i+=1
    return results
'''
def get_sens_from_keys(sen,match,keys):
    ks = get_all_keys(sen,match,keys)
    int e = 0
    for k in ks:
'''  
def get_time(text):
    time_re = r'((?:0?\d|1\d|2[0-3])\s?(?:\:|h|giờ)\s?(?:[0-5]\d)?\s?(?:[0-5]\d)?(?:am|pm)?)'
    return re.findall(time_re,text,flags=re.IGNORECASE)[0].replace('giờ',':').replace('h',':')
 #   text = open('data.txt','r').read()
#    words = text.replace('\n',' . ').split()  
# #ký tự cuối cùng của file phải có tp = 'End'   
def get_keywords(corpus,threshold):
    f = open("words.txt", "w", encoding="utf8")
    start = dt.now()
    words = corpus.replace('\n',' . ').split()
    words.append('.')
    sens = []
    sen = ""
    dic = dict()
    ws = []
    sum_of_syllabels = 0
    for word in words:
        tp,w = get_w_pos_in_sen(word)
        sum_of_syllabels+=get_num_of_sylables(w)
        sen+=(" "+w)
        if tp == "End":
            if sen.strip() != '':
                sens.append(re.sub(r"\s+"," ",sen.strip()))
            sen = ""
        if w!="":
            ws.append(w)
            if w not in dic:
                dic[w] = 1
            else:
                dic[w]+=1
    len_ = len(ws)
    k = 2
    phrdict = [dic]
    #dic2 = dict()
    while(True):
        phrs_n = dict()
        for i in range(len_):
            if i <= len_ - k:
                phrases = [" ".join([ws[i+j] for j in range(k-1)])," ".join([ws[i+j] for j in range(1,k)])]
                phrase2 = " ".join([ws[i+j] for j in range(k)])
                if phrase2 not in phrs_n:
                    phrs_n[phrase2] = 0
                    for sen in sens:
                        s = sen    
                        while(True):
                            p = s.find(phrase2)
                            if p == -1:
                                break
                            phrs_n[phrase2]+=1
                            s = s[p+1:]
                #print(str(phrases)+" ::: "+phrase2+" => "+str(phrs_n[phrase2]))
            for phrase in phrases:
                if phrs_n[phrase2] == phrdict[k-2][phrase]:
                    phrdict[k-2][phrase] = 0 
            #print("thời gian = "+str((dt.now() - start).total_seconds())+" giây")
        max_ = max(phrs_n.values())
        #print(str(max_)+" "+str(k)+" "+str(len(phrdict)))
        if(max_ < 2):
            break
        phrdict.append(phrs_n)
        k+=1
    i = 0
    data = []
    for dic in phrdict:
        data.append([])
        #print("")
        for w in dic:
            s = get_num_of_sylables(w) #số lượng âm tiết trong 1 từ
            density = dic[w] * s #mật độ xuất hiện của từ trong văn bản
            if density > threshold and dic[w] > 1 and s>0:
                #print(w+" "+str(s))
                data[i].append({'value' : w,'num_of_syllable' : s,'num' : dic[w],'density' : density * 100/sum_of_syllabels})   
        i += 1
    f.write(json.dumps(data,ensure_ascii=False))
    print("tổng thời gian = "+str((dt.now() - start).total_seconds())+" giây")
    print('số lượng âm tiết: '+str(sum_of_syllabels))
    return data