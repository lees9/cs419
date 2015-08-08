import datetime
import mysql.connector

## Just another query I was running


con = mysql.connector.connect(user='root', password='password1', database='test')
cursor = con.cursor()

query = ("SELECT FirstName, LastName, DoB FROM StarWars "
         "WHERE DoB BETWEEN %s AND %s")

born_starting = datetime.date(1931, 01, 01)
born_ending = datetime.date(1999, 12, 31)

cursor.execute(query, (born_starting, born_ending))

for (FirstName, LastName, DoB) in cursor:
  print("{} {} was born on {:%d %b %Y}".format(
    FirstName, LastName, DoB))

cursor.close()
con.close()