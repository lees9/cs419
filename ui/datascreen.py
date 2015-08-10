import urwid
import querypanel
import viewpanel
import databaseapi
import json
class Datascreen(urwid.WidgetWrap):
    signals = ['logout']
    left_panel_contents = []
    data_panel = viewpanel.Viewpanel()
    query_panel = querypanel.Querypanel()
    insert = urwid.Button("Insert Table")
    logout = urwid.Button(u"Logout")
    left_panel_contents.append(insert)
    left_panel_contents.append(logout)
    view_panel = urwid.Filler(data_panel.view,valign='top',min_height=40)
    main_footer = urwid.AttrMap(query_panel.panel, 'footer')
    left_panel = urwid.Pile(left_panel_contents)
    main_panel = urwid.BoxAdapter(urwid.Frame(body=view_panel, footer=main_footer), height=60)
    main_panel.header = urwid.Pile([urwid.Text("Database view"),urwid.Divider(div_char='-')])
    screen = urwid.Columns([urwid.AttrMap(left_panel, ('weight', 1)), urwid.AttrMap(main_panel, ('weight', 3))])

    def __init__(self):
        pass

    def refresh_left_panel(self, text,conn):
        objects = json.loads(text)
        for line in objects:
            button = urwid.Button(line)
            urwid.connect_signal(button, 'click', self.navigate, user_args=[conn,line])
            self.left_panel.contents.insert(len(self.left_panel.contents)-1,(button,self.left_panel.options()))

    def on_logout_pressed(self, button):
        raise urwid.ExitMainLoop()

    def navigate(self, caller,conn,line):
        self.data_panel.display(conn,line)
