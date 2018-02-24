import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd = "mysqlpass",
                           db = "chatlog")

    c = conn.cursor()
    print("Database connected")
    return c,conn