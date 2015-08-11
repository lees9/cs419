import urwid
import databaseapi
import main
import json

class Insertbox(urwid.WidgetWrap):
    signals = ['insert', 'failure', 'abort']
    div = urwid.Divider()
    insert_text = urwid.Button(u"Insert menu")
    insert = urwid.Button(u"Insert")
    abort = urwid.Button(u"Abort")
    iview = urwid.WidgetPlaceholder(urwid.Divider())
    pile = urwid.Pile([insert_text, div, insert, div, abort])
    top = urwid.Filler(pile, valign='top')
    def __init__(self):
        pass

    

