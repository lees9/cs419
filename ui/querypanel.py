import urwid
import databaseapi

class Querypanel(urwid.WidgetWrap):
    signals = ['execute', 'cancel']
    query_text = urwid.Edit(u"Enter query to execute :")
    status = urwid.Text(u"")
    execute = urwid.Button(u"Execute Query")
    cancel = urwid.Button(u"Cancel")
    panel = urwid.Columns([urwid.AttrMap(query_text,'weight',4),urwid.AttrMap(execute,'weight',1)])
    def __init__(self):
        pass

    # def execute_query(self,query):
    #     pass
    
    def on_execute_pressed(self, button, conn):
        if not self.execute:
            self.status.set_text("Please enter a query\n")
        else:
            try:
                user_query = self.query_text.get_edit_text()
                query_result = databaseapi.queries(user_query)
                if (query_result == 0 or query_result == -1):
                    if (query_result == 0):
                        self.status.set_text("Query succefully executed\n")
                    else:
                        self.status.set_text("Query failed. Please check your MySQL syntax\n")
                else:
                    self.status.set_text(query_result)
    
    def on_cancel_pressed(self, button):
        pass
   
   #Not sure how to implement these here??             
    #urwid.connect_signal(execute, 'execute', on_execute_pressed)
    #urwid.connect_signal(cancel, 'cancel', on_cancel_pressed)
            
