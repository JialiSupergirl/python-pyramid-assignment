import mariadb

def getConnection():
    dbConn = mariadb.connect( host="localhost", user="Jiali", password="pwd", database= "restaurant")
    cur = dbConn.cursor()
    return cur

def closeConn(cur):
    cur.close()