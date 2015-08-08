#This is only a placeholder until Matt gets the actual view panel programmed and ready to be integrated.
import urwid

class Viewpanel(urwid.WidgetWrap):
    text = urwid.Text(u"Lorem ipsum test text thing query thing something....",align='center')
    view = urwid.Padding(text,align='center')
    def __init__(self):
        pass
