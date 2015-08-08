import urwid
import connect419
import databaseapi
import json

conn = connect419.mysql()   #hardcoded connection
table = "table5"            #hardcoded tablename

#Function to get the structure of the table to show the user what fields to input
def structure(table):
    table_fields = databaseapi.showStructure(conn, table) #get json tablestructure (2nd arg should be table)
    nonJsonfields = json.loads(table_fields)    #decode json
    count = 0
    fields = []
    for i in nonJsonfields:
        count = count + 1

    last = 0
    for row in nonJsonfields:
        if (last != count-1):
            fields.append(row[0] + " " + row[1] + ", ")
        else:
            fields.append(row[0] + " " + row[1] + "\n")
        last += 1
                       
    return fields


#NEED TO MAKE ALL OF THIS INTO A CLASS INSERTBOX or INSERTPANEL
instruct = urwid.Text(("Enter for each field separated by commas. Enter NULL for each blank field\n"))
fields = urwid.Edit(structure(table))
insert = urwid.Button(u"Insert")
cancel = urwid.Button(u"Cancel")
status = urwid.Text(u"")
div = urwid.Divider()
div2 = urwid.Divider()
pile = urwid.Pile([instruct, fields, div, insert, div2, cancel, status])
body = urwid.SimpleFocusListWalker([pile])
top = urwid.Filler(pile, valign='top')

def on_insert_pressed(button):
    if not fields.get_edit_text():
        status.set_text("Please enter for each field separated by commas")
    else:
        inputInsert = fields.get_edit_text()
        forInput = inputInsert.split(", ")
        result = databaseapi.insert(conn, table, forInput)
        print result
        if (result == 0):
            print "Query executed successfully\n"
            #status.set_text("Query executed successfully\n")
        else:
            print "Query failed. Check your MySQL syntax"
            #status.set_text("Query failed. Check your MySQL syntax")
        connect419.close(conn)
        raise urwid.ExitMainLoop()
        
                
def on_cancel_pressed(button):
    connect419.close(conn)
    raise urwid.ExitMainLoop()

urwid.connect_signal(insert, 'click', on_insert_pressed)
urwid.connect_signal(cancel, 'click', on_cancel_pressed)
                
palette = [('I say', 'default,bold', 'default'),]
urwid.MainLoop(top, palette).run()

