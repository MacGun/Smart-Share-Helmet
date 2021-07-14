import pymysql as sql

DB      = sql.connect(
            user='root',
            passwd='134625',
            host='localhost',
            db='hexpod',
            charset='utf8'
        )

CUR = DB.cursor(sql.cursors.DictCursor)

def query(func, query_dict):
    func = func.lower()
    if func == 'select':
        MSG_FORM    = 'select {target} from {table} {condition};'.format(**query_dict)

    elif func =='update':
        STMT        = ",".join(['{}={}'.format(key,value) if (type(value) == type(int)) else '{}="{}"'.format(key, value) for (key,value) in query_dict.items() if key != 'condition' and key != 'table'])
        MSG_FORM    = "update {table} set {stmt} {condition}".format(table=query_dict['table'], stmt=STMT, condition=query_dict['condition'])

    return MSG_FORM


exDict1 = {"name"        : "park",
          "phone"       : "01012345678",
          "lend"        : 1,
          "table"       : "kickboard_real",
          "target"      : "*",
          "condition"   : "where id=1"
}

exDict2 = {"helmet"     : 1,
           "condition"  : "where id=1"
} 

exDict3 = {"ischarging" : 0,
           "condition"  : "where id=1"
}


