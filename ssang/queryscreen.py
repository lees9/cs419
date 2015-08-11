import urwid
import databaseapi
import json

class Queryscreen(urwid.WidgetWrap):
    signals = ['insert', 'failure', 'abort']
    div = urwid.Divider()
    query_field = urwid.Edit(u"Enter query:\n")
    query_button = urwid.Button(u"Query")
    abort = urwid.Button(u"Abort")
    status = urwid.Text(u"")
    text = urwid.Text(u"")
    iview = urwid.WidgetPlaceholder(urwid.Divider())
    pile = urwid.Pile([query_field, div, query_button, div, abort, div, status, div, text])
    top = urwid.Filler(pile, valign='top')
    def __init__(self):
        pass

    def on_query_pressed(self, conn, query_field):
        user_input = self.query_field.get_edit_text()
        result = databaseapi.queries(conn, user_input)
        if (result == -1):
            self.text.set_text(u"")
            self.status.set_text("Soemthing went really wrong")
        else:
            self.status.set_text("Query successful")
            nonjsresult = json.loads(result)

            ##blantantly copied from viewpanel. need to make more presentable with fields
            for row in nonjsresult:
                for col in row:
                    self.text.set_text(self.text.get_text()[0]+" "+str(col))
            self.text.set_text(self.text.get_text()[0]+"\n")
