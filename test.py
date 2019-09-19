import sys
import statistic_words as st
import dbconnect as dc
def insert_new_keys(keys):
    for key in keys:
        print('thêm từ khóa "'+key+'"')
        print(dc.execute(dc.defaultConnect(),"EXEC sp_DucTrinh_AddNewKeyword N'"+key+"'"))
keys = list(map(lambda i: i['Name'].lower(),dc.get_list_data(dc.defaultConnect(),'Keyword','*',None)))
insert_new_keys(['Hà Nội','TPHCM','Sài Gòn','Pasgo','Đà Nẵng','Nha Trang','Khánh Hòa','Món Huế','Ưu đãi','Ưu đãi hot','Giảm giá'])