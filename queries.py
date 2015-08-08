from connect419 import mysql, close
import json

def showTables(conn):
    tableList = []
    cur = conn.cursor()
    cur.execute("SHOW tables")
    for row in cur.fetchall():
        tableList.append(row[0])

    #jsonTable = json.dumps(tableList)
    #print jsonTable
    #return jsonTable

    return tableList

def showStructure(conn, tablename):
    structureList= []
    cur = conn.cursor()
    executeString = "DESCRIBE " + tablename
    cur.execute(executeString)
 
    for row in cur.fetchall():
        structureList.append(row)

    #jsonStructure = json.dumps(structureList)
    #print jsonStructure
    #return jsonStructure

    return structureList
    
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


def createTable(conn):
    fieldNames = ['id', 'fname', 'lname']               #get input for field names
    fieldTypes = ['INT', 'VARCHAR(25)', 'VARCHAR(25)']  #get input for each fieldtypes
    fieldNum = 3                                        #get input for number of fields
    tableName = "table5"                                #get input for table name
    primaryKey = 0                                      #get input for primary key (default to 0)
    default = ['NOT NULL', 'NULL', 'NULL']              #get default values (default to NULL except 0)
    extra = ['AUTO_INCREMENT', '', '']                  #get extra values (default to '')
    
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
    print executeString

    cur = conn.cursor()
    cur.execute('DROP Table IF EXISTS ' + tableName)
    cur.execute(executeString)


def insert(conn, table):
    tableStructure = showStructure(conn, table)
    x = len(tableStructure)
    tableFields = []                                
    fieldInputs = ['NULL', 'Michael', 'Jordan']     #get input from user. IF fields are left blank make them NULL
    tableFields_string = ""
    fieldInputs_string = ""
    
    for i in range(0,x):
        tableFields.append(tableStructure[i][0])

    tableFields_string = ', '.join(tableFields)
    fieldInputs_string = (', '.join('"' + item + '"' for item in fieldInputs))
    
    executeString = """INSERT INTO %s (%s) VALUES (%s)""" % (table, tableFields_string, fieldInputs_string)
    cur = conn.cursor()
    cur.execute(executeString)
    conn.commit()

    print "Successfully inserted row"
    print executeString


def show(conn, table):
    tableFields = ['id', 'fname', 'lname']        #get the list of table fields that user is trying to query                         
    fieldInputs = ['13', 'Michael', 'Jordan']     #get input from user. IF fields are left blank make them NULL
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
    #print executeString
    cur = conn.cursor()
    cur.execute(executeString)

    for i in cur:
        result = json.dumps(i)

    #json_result = json.dumps(result)
    print result


if __name__ == "__main__":
    conn = mysql()

    #createTable(conn)

    #x = showTables(conn)    #returns the list of tables. commented out to return json
    #print "Table: " + str(x)
    
    #y = showStructure(conn, x[1])
    #print "Structure: " + str(y)

    #insert(conn, x[1])
    table2 = "table2"
    show(conn, table2)
    
    close(conn)
