import pyodbc
def connect(createConnectSql):
    cnxn = pyodbc.connect(createConnectSql)
    return cnxn
def defaultConnect():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-KBSLCQ1\SQLEXPRESS;"
                      "Database=FutureProject;"
                      "Trusted_Connection=yes;")
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
def execute(cnxn,sql):
    try:
        cursor = cnxn.cursor()
        rs = cursor.execute(sql)
        cursor.commit()
        cursor.close()
        return rs
    except Exception as e:
        print('có lỗi '+str(e))