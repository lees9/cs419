from connect import mysql, close
import json

#Function that returns the tables in the selected database
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(sql connection)
#Returns: list of tables in the selected database in json or 1 if failed
def showTables(conn):
    tableList = []
    try:
        cur = conn.cursor()
        cur.execute("SHOW tables")
        for row in cur.fetchall():
            tableList.append(row[0])
        jsonTable = json.dumps(tableList)
        return jsonTable
    except:
        return -1



#Function that returns the structure/fields in the selected table
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(sql connection), tablename(string)
#Returns: list of fields in the selected table in json or -1 if failed
def showStructure(conn, tablename):
    structureList= []
    executeString = "DESCRIBE " + tablename

    try:
        cur = conn.cursor()
        cur.execute(executeString)
        for row in cur.fetchall():
            structureList.append(row)
        jsonStructure = json.dumps(structureList)
        return jsonStructure
    except:
        return -1



#Table class for creating tables. Used in createTable function
class table:
    fieldNames = []
    fieldTypes = []
    default = []
    extra = []
    name = ""
    fieldNum = ""
    primaryKey = ""
    def __init__(self, name, fieldNum, fieldNames, fieldTypes, default, extra, primaryKey):
        self.name = name
        self.fieldNum = fieldNum
        self.primaryKey = primaryKey
        for i in range(0, self.fieldNum):
            self.fieldNames.append(fieldNames[i])
            self.fieldTypes.append(fieldTypes[i])
            self.default.append(default[i])
            self.extra.append(extra[i])



#Function to create a new table in the MySQL database
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(mysql connection), fieldNames(list), fieldTypes(list), fieldNum(int), tableName(string), primaryKey(int), default(list), extra(list)
#Returns: 0 for success, -1 for failed
def createTable(conn, fieldNames, fieldTypes, fieldNum, tableName, primaryKey, default, extra):

##SAMPLE INPUT TO SHOW THE FORMAT THAT THE ARGUMENTS TO THIS FUNCTION WILL REQUIRE
##    fieldNames = ['id', 'fname', 'lname']               #get input for field names
##    fieldTypes = ['INT', 'VARCHAR(25)', 'VARCHAR(25)']  #get input for each fieldtypes
##    fieldNum = 3                                        #get input for number of fields
##    tableName = "table5"                                #get input for table name
##    primaryKey = 0                                      #get input for primary key (default to 0)
##    default = ['NOT NULL', 'NULL', 'NULL']              #get default values (default to NULL except 0)
##    extra = ['AUTO_INCREMENT', '', '']                  #get extra values (default to '')
    
    newTable = table(tableName, fieldNum, fieldNames, fieldTypes, default, extra, primaryKey)

    x = ""
    for i in range(0, newTable.fieldNum):
        if newTable.extra[i] == '':
            x += newTable.fieldNames[i] + " " + newTable.fieldTypes[i] + " " + newTable.default[i] + ", "
        else:
            x += newTable.fieldNames[i] + " " + newTable.fieldTypes[i] + " " + newTable.default[i] + " " + newTable.extra[i] + ", "

        if i == newTable.fieldNum-1:
            x += "PRIMARY KEY (" + newTable.fieldNames[newTable.primaryKey] + ")"

    executeString = """CREATE TABLE %s (%s)""" % (newTable.name, x)
    try:
        cur = conn.cursor()
        cur.execute('DROP Table IF EXISTS ' + tableName)
        cur.execute(executeString)
        return 0
    except:
        return -1



#Function to insert a row into the MySQL table
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(mysql connection), table(string), fieldInput(list)
#Returns: 0 for success, -1 for failed
def insert(conn, table, fieldInputs):

##SAMPLE INPUT TO SHOW THE FORMAT THAT THE ARGUMENTS TO THIS FUNCTION WILL REQUIRE
##    fieldInputs = ['NULL', 'Rachel', 'McAdams']     #get input from user. IF fields are left blank make them NULL

    jsontableStructure = showStructure(conn, table)
    tableStructure = json.loads(jsontableStructure)
    x = len(tableStructure)
    tableFields = []                                
    tableFields_string = ""
    fieldInputs_string = ""
    
    for i in range(0,x):
        tableFields.append(tableStructure[i][0])

    tableFields_string = ', '.join(tableFields)
    fieldInputs_string = (', '.join('"' + item + '"' for item in fieldInputs))
    executeString = """INSERT INTO %s (%s) VALUES (%s)""" % (table, tableFields_string, fieldInputs_string)

    try:
        cur = conn.cursor()
        cur.execute(executeString)
        conn.commit()
        return 0
    except:
        return -1



#Function that returns row(s) from a specific query. Analogous to the SEARCH tab in phpMyAdmin
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(mysql connection), tableFields(list), fieldInputs(list)
#Returns: The row(s) from the execute query in json or -1 for failed
def show_row(conn, table, tableFields, fieldInputs):

##SAMPLE INPUT TO SHOW THE FORMAT THAT THE ARGUMENTS TO THIS FUNCTION WILL REQUIRE
##    tableFields = ['id', 'fname', 'lname']        #get the list of table fields that user is trying to query                         
##    fieldInputs = ['13', 'Michael', 'Jordan']     #get input from user. IF fields are left blank make them NULL
    
    tableFields_string = ""
    fieldInputs_string = ""
    query = ""
    x = len(tableFields)
    result = []
    
    for i in range(0, x):
        if i == x-1:
            query += tableFields[i] + '=' + '"' + fieldInputs[i] + '"'
        else:
            query += tableFields[i] + '=' + '"' + fieldInputs[i] + '"' + " and "
        
    executeString = """SELECT * FROM %s WHERE (%s)""" % (table, query)

    try:
        cur = conn.cursor()
        cur.execute(executeString)
        for i in cur:
            result.append(i)
        json_result = json.dumps(result)
        return json_result
    except:
        return -1



#Function that returns all the rows in the "selected/highlighted" table
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(mysql connection), table(string)
#Returns: all rows in the specified table in json or returns -1 if error
def show_all(conn, table):
    executeString = """SELECT * FROM %s""" % (table)
    result = []
    try:
        cur = conn.cursor()
        cur.execute(executeString)
        for i in cur:
            result.append(i)
        jsonresult = json.dumps(result)
        return jsonresult
    except:
        return -1



#Function submits a free written query to the mysql database
#Preconditions: MySQL connection
#Postconditions: None
#Arguments: conn(mysql connection), query(string)
#Returns: For select statements returns result in json or -1 for failed. For other statements: 0 for success, -1 for failed
def queries(conn, query):
    result = []
    query_list = query.split()
    query_zero_cap = query_list[0].upper()
    if (query_zero_cap == "SELECT"):
        try:
            cur = conn.cursor()
            cur.execute(query)
            for i in cur:
                result.append(i)
                jsonresult = json.dumps(result)
            return jsonresult
        except:
            return -1
    else:
        try:
            cur = conn.cursor()
            cur.execute(query)
            return 0
        except:
            return -1


def delete(conn, table, idNum):
    if (idNum.isdigit()):
        idVal = int(idNum)
    else:
        return -1
    
    query = """DELETE FROM %s WHERE id=%i""" % (table, idVal)
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return 0
    except:
        return -1

#just testing these functions to see output. disregard.
if __name__ == "__main__":
    conn = mysql()

    query = "select * FROM table2"
    x = queries(conn, query)
    print x
    
    close(conn)
