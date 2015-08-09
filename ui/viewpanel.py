#This is only a placeholder until Matt gets the actual view panel programmed and ready to be integrated.
import urwid
import json
import databaseapi
class Viewpanel(urwid.WidgetWrap):
    text = urwid.Text(u"Lorem ipsum test text thing query thing something....",align='center')
    view = urwid.Padding(text,align='center')
    def display(self,conn,line):
        self.text.set_text("")
        results = json.loads(databaseapi.show_all(conn,line))
        for row in results:
            self.text.set_text(self.text.get_text()+"\n"+row)
    def __init__(self):
        pass
