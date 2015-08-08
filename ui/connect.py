import datetime
#import mysql.connector
from mysql.connector import (connection)


#connect to mysql
def mysql():

    print "Connecting to database"
    conn = connection.MySQLConnection(user="root", password="123", host="localhost", database="test")
    if conn:
        print "Connected!"
    else:
        print "Failed to connect"
    
    #cur = conn.cursor()

    #Specific to the database I have in my localhost
    #cur.execute("SELECT title FROM film WHERE length > 184")
    #for row in cur.fetchall() :
        #print "Title of movie: " + row[0]

    return conn

#close connection
def close(conn):
    conn.close()
    print "Connection closed"

#connect to postgresql
def postgre():
    print "Youve reached the function for postgresql"


if __name__ == '__main__':

    db_select = input("Select 1 for MySQL or 2 for postgreSQL: ")
    if db_select == 1:
        a = mysql()
    else:
        postgre()

    close(a)
