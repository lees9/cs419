#!/usr/bin/python
import datetime
import MySQLdb


#connect to mysql
def mysql(username,password,database):

    print "Connecting to database"
    conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="sql_assignment")

    if conn:
        print "Connected!"
    else:
        print "Failed to connect"
    
    cur = conn.cursor()

    #Specific to the database I have in my localhost
    cur.execute("SELECT title FROM film WHERE length > 184")
    for row in cur.fetchall() :
        print "Title of movie: " + row[0]
    ####
        
    print "Connection closed"

#connect to postgresql
def postgre():
    print "Youve reached the function for postgresql"


def close():
    conn.close()


if __name__ == '__main__':

    db_select = input("Select 1 for MySQL or 2 for postgreSQL: ")
    if db_select == 1:
        mysql()
    else:
        postgre()