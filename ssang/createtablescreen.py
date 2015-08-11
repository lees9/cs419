import urwid
import databaseapi

class CreateTableScreen(urwid.WidgetWrap):
    signals = ['inserted', 'failure','abort']
    table_name = urwid.Edit("What is the name for your table?\n", u"")
    columns = urwid.IntEdit("How many columns do you want to insert?\n")
    div = urwid.Divider()
    next_step = urwid.Button(u"Next")
    abort = urwid.Button(u"Abort")
    insert_view = urwid.WidgetPlaceholder(urwid.Divider())
    pile = urwid.Pile([table_name, columns, div, next_step, abort])
    create_button = urwid.Button("Create Table")
    top = urwid.Filler(pile, valign='top')
    def __init__(self):
        pass

##SAMPLE INPUT TO SHOW THE FORMAT THAT THE ARGUMENTS TO THIS FUNCTION WILL REQUIRE
##    fieldNames = ['id', 'fname', 'lname']               #get input for field names
##    fieldTypes = ['INT', 'VARCHAR(25)', 'VARCHAR(25)']  #get input for each fieldtypes
##    fieldNum = 3                                        #get input for number of fields
##    tableName = "table5"                                #get input for table name
##    primaryKey = 0                                      #get input for primary key (default to 0)
##    default = ['NOT NULL', 'NULL', 'NULL']              #get default values (default to NULL except 0)
##    extra = ['AUTO_INCREMENT', '', '']                  #get extra values (default to '')
    def input_columns(self,tablename,num_cols,conn,button):
        table_header = urwid.Text(u"Please insert the column and values for the table: "+tablename)
        input_pile = urwid.Pile([table_header])
        for i in range(0,num_cols):
            rowPile = urwid.Pile([urwid.EditText("Column Name"),urwid.EditText("Column Type"),urwid.IntText("Length"),
                                  urwid.Checkbox("Primary"),urwid.EditText("Extra")])
            input_pile.contents.append(rowPile)
        input_pile.contents.append((self.create_button,input_pile.options()))
        input_pile.contents.append((self.abort,input_pile.options()))
        result_view = urwid.Filler(input_pile)
        urwid.connect_signal(self.create_button,'click',self.insert,user_args=[tablename,conn])
        self.insert_view.original_widget = result_view



    def insert(self,tablename,conn,button):

        #TODO: Implement
        pass
