import pyodbc
def connect(createConnectSql):
    cnxn = pyodbc.connect(createConnectSql)
    return cnxn
def defaultConnect():
    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=FutureProject;UID=sa;PWD=Duc20091994;")
    return cnxn
def get_list_data(cnxn,table,params,size):
    keys = None
    if params == '*':
        keys = '*'
    else:
        keys = ','.join([item for item in params])
    sql = "SELECT "+('' if size == None else ('TOP '+size+" "))+keys+" FROM "+table
    cursor = cnxn.cursor()
    rows = cursor.execute(sql).fetchall()
    data = []
    for row in rows:
        item = dict()
        for r in cursor.columns(table= table):
            item[r.column_name] = getattr(row, r.column_name)
        data.append(item)
    cursor.close()
    return data
'''
get list data
@cnxn connection
@sql the query string 
'''
def get_list(cnxn,sql):
    columns = []
    data = []
    cursor = cnxn.cursor()
    rows = cursor.execute(sql)
    for column in rows.description:
        columns.append(column[0])
    len_ = len(columns)
    for row in rows:
        item = dict()
        for i in range(len_):
            item[columns[i]] = row[i]
        data.append(item)
    cursor.close()
    return data

def execute(cnxn,sql):
    try:
        cursor = cnxn.cursor()
        rs = cursor.execute(sql).fetchone()
        cursor.commit()
        cursor.close()
        return rs
    except Exception as e:
        print('có lỗi '+str(e))