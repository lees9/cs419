import urwid
import databaseapi

class Querypanel(urwid.WidgetWrap):
    signals = ['execute', 'cancel']
    query_text = urwid.Edit(u"Enter query to execute :")
    status = urwid.Text(u"")
    execute = urwid.Button(u"Execute Query")
    cancel = urwid.Button(u"Cancel")
    panel = urwid.Columns([urwid.AttrMap(query_text,'weight',4),urwid.AttrMap(execute,'weight',1)])

    def on_cancel_pressed(self, button):
        self._emit('cancel')

    def __init__(self):
        pass

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
            except:
                self.status.set_text("Something has gone horribly wrong.")
