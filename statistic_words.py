import re,json
from datetime import datetime as dt
from unidecode import unidecode
import math
vowels = ['a','e','i','o','u','y']

'''
I.Phương pháp luận
    * Để hiểu được ý định người dùng khi họ nhập vào 1 đoạn text,ta phải:
        B1: lọc được tất cả các từ khóa trong đoạn text của người dùng
        B2: dựa vào các từ khóa đó

II.Một số khái niệm được dùng
1. Mật độ từ khóa trong 1 vb
  = (số lần xuất hiện từ khóa * số âm tiết từ khóa) * 100 /tổng số âm tiết trong vb 
2. Độ khớp giữa 2 từ khóa = alpha ^ f(các tham số so sánh giữa 2 từ khóa)
3. Alpha của từ khóa : là giá trị dùng để xác định độ khớp từ khóa dựa vào công thức trên
 => giá trị này sẽ được thay đổi(huấn luyện) để lọc các từ khóa chính xác
 => Giá trị mặc định alpha là 0.95 nếu ko set
'''


#Có phải là số ko
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
   # if is_number(word):
   #     return '@num'
    return unidecode(word)
#Trả về số âm tiết của 1 từ,cụm từ hoặc 1 câu
#vd: "món huế" có 2 âm tiết,"hello" có 2 âm tiết,"món ăn ngon" có 3 âm tiết
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
#Lấy kí tự đầu tiên của 1 cụm từ
# bắt đầu bằng chữ cái trong bảng alphabet trả về chữ cái đó VD : "món huế" => mh
# bắt đầu bằng chữ số hoặc ký tự đặc biệt => trả về @
# chuỗi là rỗng không trả về gì cả
def get_first_letter(phrase):
    phrase = phrase.lower().strip()
    if phrase == '':
        return '\0'
    words = phrase.split()
    if len(words) == 1:
        if not (words[0][0].isalpha() or words[0][0].isdigit()):
            return '@'
        return words[0][0]
    f = ''
    for word in words:
        f+=get_first_letter(word)
    return f
#trả về tập nguyên âm
def get_vowels(phrase):
    phrase = phrase.lower().strip()
    if phrase == '':
        return []
    words = phrase.split()
    vls = []
    if len(words) == 1:
        if not words[0].isalpha() and words[0].isalnum() :
            return words
        vl = ''
        w = words[0] + ' '
        for l in w:
            if u(l) in vowels:
                vl+=l
            else:
                if vl != '':
                    vls.append(vl)
                vl = ''
        return vls if len(vls) > 0 else ['']
    for word in words:
        vls+=get_vowels(word)
    return vls
# kiểm tra xem từ nhập vào có có chứa ký tự đặc biệt ko
# nếu chỉ chứa số + chữ => true
# có chứa ký tự đặc biệt => false
def is_word(w):
    if is_number(w):
        return True
    for l in w:
        if not l.isalpha():
            return False
    return True
#trả về vị trí của từ trong 1 câu
#VD: 
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
'''
buffet buftef
expect điểm kì vọng 0.9,0.89....
gamma hệ số huấn luyện
c1[0] = c1[1] * c1[9] + c1[2] * c1[10] + c1[3] * c1[11] + c1[4] * c1[12] + c1[5] * c1[13] + c1[6] * c1[14] + c1[7] * c1[15] + c[8] * c[16]
c2[0] = c2[1] * c2[9] + c2[2] * c2[10] + c2[3] * c2[11] + c2[4] * c2[12] + c2[5] * c2[13] + c2[6] * c2[14] + c2[7] * c2[15] + c[8] * c[16]

expect ** 8 ~ c1[0] ** 8 * multiply(1 + c1[j] / c2[i]) với (1 <= i <= 8 , 9<= j <= 16)

if sum(c[j]) == 0:
    dx1[i] = c1'[i] - c1[i] = 0
else
    R = (expect / c1[0]) ** (8/sum_a1)
    dx1[i] = c1'[i] - c1[i] = r ^ c1[j] * c1[i] / c1[j]
expect / c1[0]
'''
def training(w1,w2,expect,gamma = 0.01,alphas1 = None,alphas2 = None):
    c1 = compare_ver2(w1,w2,alphas1)
    c2 = compare_ver2(w2,w1,alphas2)
    
    if alphas1 is None:
        alphas1 = dict()
    if alphas2 is None:
        alphas2 = dict()
    
    #print(f'c1 = {c1[0]} --- c2 = {c2[0]} --- result = {compare_2_ways_ver2(w1,w2,alphas1,alphas2)[0]}')

    sum_a1 = sum(c1[9:])
    sum_a2 = sum(c2[9:])

    if sum_a1 == 0:
        for i in range(8):
            alphas1[i] = c1[i+1]
    else:
        R1 = (expect / c1[0]) ** (8/sum_a1)
        A11 = 1
        A12 = 1
        for i in range(1,9):
            if c1[i+8] == 0:
                alphas1[i-1] = c1[i]
            else:
                d = (R1 ** c1[i+8] - 1) * c1[i] / c1[i+8]
                alphas1[i-1] = c1[i] + d * gamma
                A11 = A11 * (alphas1[i-1] ** c1[i+8])
                A12 = A12 * (c1[i] ** c1[i+8] * (1 + c1[i + 8] * d * gamma / c1[i]))
        
    if sum_a2 == 0:
        for i in range(8):
            alphas2[i] = c2[i+1]
    else:
        R2 = (expect / c2[0]) ** (8/sum_a2)
        A21 = 1
        A22 = 1
        for i in range(1,9):
            if c2[i+8] == 0:
                alphas2[i-1] = c2[i]
            else:
                d = (R2 ** c2[i+8] - 1) * c2[i] / c2[i+8]
                alphas2[i-1] = c2[i] + d * gamma
                A21 = A21 * (alphas2[i-1] ** c2[i+8])
                A22 = A22 * (c2[i] ** c2[i+8] * (1 + c2[i + 8] * d * gamma / c2[i]))
        #print(f'1. {A21 ** (1/8)} -- {A22 ** (1/8)}')
    return alphas1,alphas2
def compare_2_ways_ver2(w1,w2,alphas1 = None,alphas2 = None):
    c1 = compare_ver2(w1,w2,alphas1)
    c2 = compare_ver2(w2,w1,alphas2)
    return [(c1[i] * c2[i]) ** (1/2) for i in range(len(c1))]


'''
    Trả về điểm(xác xuất + điểm từng hạng mục tương ứng)
'''
def compare_ver2(w1,w2,alphas = dict()):
    defaultAlpha = 0.9
    w1,w2 = [re.sub(r'\s+',' ',w1.lower().strip()),re.sub(r'\s+',' ',w2.lower().strip())]
    if w1.replace(' ','') == w2.replace(' ',''):
        return (1,defaultAlpha,defaultAlpha,defaultAlpha,defaultAlpha,defaultAlpha,defaultAlpha,defaultAlpha,defaultAlpha)
    if alphas is None:
        alphas = dict()
    i1 = len(w1),get_num_of_sylables(w1),get_first_letter(w1),get_vowels(w1)
    i2 = len(w2),get_num_of_sylables(w2),get_first_letter(w2),get_vowels(w2),list(map(lambda item : u(item),i1[3]))
    d = 1
    #độ lệch về chiều dài giữa w1,w2
    x1 = abs(i1[0] - i2[0])
    #độ lệch về số lượng âm tiết w1,w2
    x2 = abs(i1[1]-i2[1])
    #độ lệch về các chữ cái đầu của các từ
    x3 = int(not i1[2] == i2[2])
    #độ lệch về thứ tự các chữ cái đầu w1,w2
    x4 = int(not u(i1[2]) == u(i2[2]))
    #độ lệch về chữ cái đầu tiên w1,w2
    x5 = 0
    for fl in i1[2]:
        x5+=int(not u(fl) in u(i2[2]))
    #độ lệch về nguyên âm
    x6 = 0
    for vl in i1[3]:
        x6+=(int(vl not in i2[3]) + 2*int(u(vl) not in i2[4]))
    # độ lệch về thứ tự các chữ cái w1,w2 dạng utf-8
    x7 = 0
    # độ lệch về thứ tự các chữ cái w1,w2 dạng ascii
    x8 = 0
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
        x7 += int(m<=map_pos)
        map_pos = m
    letters = dict()
    map_pos = - 1
    for l in u(w1):
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(u(w2),l,letters[l])
        x8 += int(m<=map_pos)
        map_pos = m
    a1 = alphas.get(0,defaultAlpha)
    a2 = alphas.get(1,defaultAlpha)
    a3 = alphas.get(2,defaultAlpha)
    a4 = alphas.get(3,defaultAlpha)
    a5 = alphas.get(4,defaultAlpha)
    a6 = alphas.get(5,defaultAlpha)
    a7 = alphas.get(6,defaultAlpha)
    a8 = alphas.get(7,defaultAlpha)
    d = a1**x1 * a2**x2 * a3**x3 * a4**x4 * a5**x5 * a6**x6 * a7**x7 * a8**x8
   #print(f'd = {d} \n a1 ^ x1 = {a1**x1} \n a2^x2 = {a2**x2} \n a3^x3 = {a3**x3} \n a4^x4 = {a4**x4} \n a5^x5 = {a5**x5} \n a6^x6 = {a6**x6} \n a7^x7 = {a7**x7} \n a8^x8 = {a8**x8}')
    return (d ** (1/8),a1,a2,a3,a4,a5,a6,a7,a8,x1,x2,x3,x4,x5,x6,x7,x8)
'''
So sánh độ khớp của 2 từ với nhau(0 -> 1 tương ứng 0 => 100%)
[
    alpha # 'len_ch',
    alpha # 'num_of_syll',
    alpha # 'first_letter_utf8',
    alpha ^ 2  # 'first_letter_ascii',
    alpha # 'vowels_utf8',
    alpha ^ 2  # 'vowels_ascii',
    alpha ^ 2 # 'hierachy_utf8',
    alpha ^ 2  # 'hierachy_ascii'
]
#độ mạnh của từ khóa
#giá trị mặc định alpha = 0.95
'''
def compare_2_ways(w1,w2,alpha = None):
    return (compare(w1,w2,alpha) + compare(w2,w1,alpha))/2
def compare(w1,w2,alpha = None,fence = None):
    w1,w2 = [re.sub(r'\s+',' ',w1.lower().strip()),re.sub(r'\s+',' ',w2.lower().strip())]
    if w1.replace(' ','') == w2.replace(' ',''):
        return 1
    if alpha is None:
        alpha = 0.95
    if fence is None:
        fence = 0
    i1 = len(w1),get_num_of_sylables(w1),get_first_letter(w1),get_vowels(w1)
    i2 = len(w2),get_num_of_sylables(w2),get_first_letter(w2),get_vowels(w2),list(map(lambda item : u(item),i1[3]))
    d = alpha**abs(i1[0] - i2[0]) * alpha**abs(i1[1]-i2[1]) * alpha**int(not i1[2] == i2[2])*alpha**(2*int(not u(i1[2]) == u(i2[2])))
    for fl in i1[2]:
        d*=alpha**(2*int(not u(fl) in u(i2[2])))
    for vl in i1[3]:
        d*=(alpha**int(vl not in i2[3]) * alpha**(2*int(u(vl) not in i2[4])))
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
        d*=(alpha**int(m<=map_pos))
        map_pos = m
    letters = dict()
    map_pos = - 1
    for l in u(w1):
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(u(w2),l,letters[l])
        d*=(alpha**(2*int(m<=map_pos)))
        map_pos = m
      #  print(l+" "+" "+str(d))
    #print(str(d)+' === '+str(pivot))
    return d**(0.5/min(i1[1],i2[1]))
#if w1 contain w2
#kiểm tra tất cả các khớp của w2 có nằm trong w1 hay không
def contain_compare(w1,w2):
    #loại bỏ khoảng trắng và chuyển text thành dạng chữ thường
    w1,w2 = [re.sub(r'\s+',' ',w1.lower().strip()),re.sub(r'\s+',' ',w2.lower().strip())]
    w1 = w1.replace(" ","")
    w2 = w2.replace(" ","")
    d = 1
    map_pos = -1
    #lưu các chữ cái của w2
    letters = dict()
    #liệt kê các chữ cái @l của w2
    for l in w2:
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        #tìm vị trí của chữ cái @l tiếp theo trong w1
        m = find_sub_str_with_pos(w1,l,letters[l])
        #với 1 substring có dạng @l1@l2 (VD: 'an') trong W2
        # @m là vị trí của @l2 
        #nếu @m <= @map_pos tức là vị trí của @l2 trong w1 < vị trí @l1 trong W1 thì d = d * 0.99
        #nếu @m - @map_pos = 1 tức @l1@l2 cũng đang tồn tại trong w1 
        d*=(0.99**(int(m<=map_pos)+int(m - map_pos != 1)))
        map_pos = m
    letters = dict()
    map_pos = -1
    for l in u(w2):
        if l not in letters:
            letters[l] = 1
        else:
            letters[l]+=1
        m = find_sub_str_with_pos(u(w1),l,letters[l])
        d*=(0.9**(int(m<=map_pos)+int(m - map_pos != 1)))
        map_pos = m
    return d**(0.5/get_num_of_sylables(w2))
#trả về vị trí @_sub trong chuỗi @_str lần thứ @pos
#VD: lấy substring 'àn' của string 'đặt bÀN nhà hÀNg' thứ 2 là 13
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

#lấy tất cả các match(các key trong db khớp với @sen)
def get_all_keys(sen,match,keys):
    if match <0 or match > 1:
        print("match must be from 0 to 1")
        return []
    results = []
    #keys = sorted(keys,key=len,reverse=True)
    ws = sen.lower().split()
    i = 0
    n = len(ws)
    while(i < n):
        if not ws[i].isalpha():
            results.append({
                "key":'_notalpha_'+ws[i]+'_'+str(i)+'_'+str(len(ws[i])),
                "matched_token": "",
                "begin": i,
                "len": 1,
                "alpha": 0.95,
                "score": 1
            })
     #       results.append([('_notalpha_'+ws[i]+'_'+str(i)+'_'+str(len(ws[i])),i,i+1,1)])
     #       i+=1
     #       continue
        temps = []
        for key in keys:
            keyName = key['Name']
            keyAlpha = float(key['Alpha'])
            if u(keyName[0]) == u(ws[i][0]) :
                rs = dict() 
                if len_sen(keyName) == 1:
                    f = compare_2_ways(ws[i],get_word_by_pos(keyName,0),keyAlpha)
                    if f > match:
                        rs = {
                            "key":keyName,
                            "matched_token": ws[i],
                            "begin": i,
                            "len": 1,
                            "alpha": keyAlpha,
                            "score": f
                        }
                        #rs = (key,i,i+1,compare_2_ways(ws[i],get_word_by_pos(key,0)))
                else:
                    j = 0
                    sub_sen = ''
                    len_key = len_sen(keyName)
                    while(i+j < n):
                        sub_sen+=(ws[i+j]+" ")
                        cp = compare_2_ways(sub_sen,keyName,keyAlpha)
                        if j > len_key +2:
                            break
                        #print("key: "+key+"\n sub_sen: "+sub_sen+"\n score: "+str(cp))
                        #Chọn ra match khớp nhất với sen
                        #match tốt nhất sẽ là match có điểm so sánh(cp) lớn nhất(trong TH tìm đc match mới có cp = match cũ,lấy match có chiều dài lớn hơn)
                        if cp > match:
                            #nếu chưa có match nào,tạo mới 1 match mới bao gồm key,vị trí bắt đầu(i),vị trí kết thúc(i+j),điểm so sánh(cp)
                            if len(rs) == 0:
                                    rs = {
                                        "key":keyName,
                                        "matched_token": sub_sen,
                                        "begin": i,
                                        "len": j+1,
                                        "alpha": keyAlpha,
                                        "score": cp
                                    }
                                   # rs = (key,i,i+j+1,cp)
                            #nếu đã có match cũ,kiểm tra match mới
                            else:
                                #if rs[3] < cp or (rs[3] == cp and (i+j+1) > rs[2]):
                                #    rs = (key,i,i+j+1,cp)
                                if rs["score"] < cp or (rs["score"] == cp and (j+1) > rs["len"]):
                                     rs = {
                                        "key":keyName,
                                        "matched_token": sub_sen,
                                        "begin": i,
                                        "len": j+1,
                                        "alpha": keyAlpha,
                                        "score": cp
                                    }
                        j += 1
                if len(rs) > 0:
                    temps.append(rs)
                    if rs["begin"]+rs["len"] > n:
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
#lọc text dạng thời gian trong 1 đoạn text
def get_time(text):
    time_re = r'((?:0?\d|1\d|2[0-3])\s?(?:\:|h|giờ)\s?(?:[0-5]\d)?\s?(?:[0-5]\d)?(?:am|pm)?)'
    return re.findall(time_re,text,flags=re.IGNORECASE)[0].replace('giờ',':').replace('h',':')
#trả về các từ khóa của 1 bài viết từ 1 corpus(có thể là đoạn văn,bài văn,đoạn text trong 1 file văn bản nào đó)
#corpus : đoạn văn cần lấy từ khóa 
#density_threshold (0 - 100) : lọc các từ khóa có mật độ > density_threshold
def get_keywords(corpus,density_threshold):
    f = open("words.txt", "w", encoding="utf8")
    start = dt.now()
    words = corpus.replace('\n',' . ').split()
    words.append('.')
    #tập các câu mà đoạn văn đó được hợp thành
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
        #biến tạm để lưu tất cả các cụm từ có i từ
        phrs_n = dict()
        for i in range(len_):
            if i <= len_ - k:
                phrases = [" ".join([ws[i+j] for j in range(k-1)])," ".join([ws[i+j] for j in range(1,k)])]
                phrase2 = " ".join([ws[i+j] for j in range(k)])
                if phrase2 not in phrs_n:
                    phrs_n[phrase2] = 0
                    #liệt kê tất cả các câu trong bài văn
                    for sen in sens:
                        s = sen    
                        while(True):
                            #tìm xem cụm từ đang xét xuất hiện mấy lần trong câu @sen
                            #nếu không xuất hiện thì next sang câu khác
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
            density = dic[w] * s *100 / sum_of_syllabels #mật độ xuất hiện của từ trong văn bản
            if density > density_threshold and dic[w] > 1 and s>0:
                #print(w+" "+str(s))
                data[i].append({'value' : w,'num_of_syllable' : s,'num' : dic[w],'density' : density})   
        i += 1
    f.write(json.dumps(data,ensure_ascii=False))
    print("tổng thời gian = "+str((dt.now() - start).total_seconds())+" giây")
    print('số lượng âm tiết: '+str(sum_of_syllabels))
    return data