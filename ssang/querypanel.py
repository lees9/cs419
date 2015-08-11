##import urwid
##import databaseapi
##
##class Querypanel(urwid.WidgetWrap):
##    signals = ['execute', 'failure', 'abort']
##    query_text = urwid.Edit(u"Enter query to execute:\n")
##    div = urwid.Divider()
##    execute = urwid.Button(u"Execute Query")
##    abort = urwid.Button(u"Abort")
##    status = urwid.Text(u"")
##    qview = urwid.WidgetPlaceholder(urwid.Divider())
##    pile = urwid.Pile([query_text, div, execute, div, abort, div, status])
##    top = urwid.Filler(pile, valign='top')
##    #panel = urwid.Columns([urwid.AttrMap(query_text,'weight',4),urwid.AttrMap(execute,'weight',1)])
##    def __init__(self):
##        pass
##
##    def on_execute_pressed(self, button, conn):
##        if not self.execute:
##            self.status.set_text("Please enter a query\n")
##        else:
##            try:
##                user_query = self.query_text.get_edit_text()
##                query_result = databaseapi.queries(user_query)
##                if (query_result == 0 or query_result == -1):
##                    if (query_result == 0):
##                        self.status.set_text("Query succefully executed\n")
##                    else:
##                        self.status.set_text("Query failed. Please check your MySQL syntax\n")
##                else:
##                    self.status.set_text(query_result)
##            except:
##                self.status.set_text("Something has gone horribly wrong.")

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
