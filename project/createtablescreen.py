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

    input_pile = urwid.Pile([div])
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
    def input_columns(self,conn,button):
        table_header = urwid.Text(u"Please insert the column and values for the table: " +
                                  self.table_name.get_edit_text())
        self.input_pile.contents.append((table_header,self.input_pile.options()))
        rowPile = urwid.Pile([])
        columns_count = int(self.columns.get_edit_text())
        for i in range(0,columns_count):
            rowPile = urwid.Pile([(urwid.Edit("Column Name")),(urwid.Edit("Column Type")),
                                  (urwid.Edit("Primary")),(urwid.Edit("Default")),(urwid.Edit("Extra"))])
            self.input_pile.contents.append((rowPile,self.input_pile.options()))
        self.input_pile.contents.append((self.create_button,self.input_pile.options()))
        self.input_pile.contents.append((self.abort,self.input_pile.options()))
        result_view = urwid.Filler(self.input_pile)
        urwid.connect_signal(self.create_button,'click',self.insert,user_args=[self.table_name.get_edit_text(),conn])
        self.top.original_widget = urwid.Padding(self.input_pile,('relative',100),'pack')
        self.input_pile.set_focus(2)


    def insert(self,tablename,conn,button):
        table_definition = []
        for i in range(1,len(self.input_pile.contents)):
            if isinstance(self.input_pile.contents[i][0], urwid.Pile):
                column_definition = []
                for j in range(0, len(self.input_pile.contents[i][0].contents)):
                    if isinstance(self.input_pile.contents[i][0][j],urwid.Edit):
                        column_definition.append(self.input_pile.contents[i][0][j].get_edit_text())
                table_definition.append(column_definition)
                
        colNames = []
        colTypes = []
        defaults = []
        extras = []
        pk = 0
        for column in range(0,len(table_definition)):
            colNames.append(table_definition[column][0])
            colTypes.append(table_definition[column][1])
            if table_definition[column][2].lower()=='yes' or table_definition[column][2].lower() == 'true':
                pk = column
            defaults.append(table_definition[column][3])
            extras.append(table_definition[column][4])
        
        databaseapi.createTable(conn,colNames,colTypes,len(table_definition),tablename,pk,defaults,extras)
        self._emit('inserted')        
