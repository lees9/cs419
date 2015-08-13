import urwid
import json
import databaseapi
class Viewpanel(urwid.WidgetWrap):
    text = urwid.Text(u"",align='center')
    view = urwid.Padding(text,align='center')
    def display(self,conn,line):
        self.text.set_text("")
        describe = json.loads(databaseapi.showStructure(conn,line))
        for col in describe:
            self.text.set_text(self.text.get_text()[0]+" "+str(col))
            self.text.set_text(self.text.get_text()[0]+"\n")
        jstext = databaseapi.show_all(conn,line)
        results = json.loads(jstext)
        for row in results:

            for col in row:
                self.text.set_text(self.text.get_text()[0]+" "+str(col))
            self.text.set_text(self.text.get_text()[0]+"\n")
    def __init__(self):
        pass
