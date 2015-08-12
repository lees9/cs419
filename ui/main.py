import urwid
import databaseapi
import datascreen
import loginbox
import createtablescreen
import json
from loginbox import LoginPopupLauncher

conn = None
main_screen = None
popup_launcher = None
spacer = urwid.Divider()
box = loginbox.LoginBox()
main_screen = urwid.Filler(spacer)
data_screen = datascreen.Datascreen()
create_screen = createtablescreen.CreateTableScreen()
popup_launcher = LoginPopupLauncher(main_screen)
def main():
    urwid.connect_signal(box.login, 'click', box.on_login_pressed, user_args=[conn])
    urwid.connect_signal(box, 'success', on_login_success)
    popup_launcher.original_widget = urwid.WidgetPlaceholder(box.top)
    urwid.connect_signal(box.exit, 'click', box.on_exit_pressed)
    loop = urwid.MainLoop(popup_launcher, pop_ups=True)
    loop.run()


def on_login_success(object,conn):
    data_screen.refresh_left_panel(databaseapi.showTables(conn), conn)
    tables = json.loads(databaseapi.showTables(conn))
    cols = databaseapi.showStructure(conn,tables[0])
    for col in cols:
        data_screen.data_panel.text.set_text(data_screen.data_panel.text.get_text()[0]+" "+str(col))
    data_screen.data_panel.text.set_text(databaseapi.showStructure(conn, tables[0]))
    popup_launcher.original_widget = urwid.WidgetPlaceholder(urwid.Filler(data_screen.screen))
    urwid.connect_signal(data_screen.logout, 'click', data_screen.on_logout_pressed)
    urwid.connect_signal(data_screen.insert,'click', on_create_table,user_args=[conn])


def on_login_failure(args):
    #TODO: Message for GTFO
    pass

def on_create_table(conn,button):
    urwid.connect_signal(create_screen.next_step, 'click', create_screen.input_columns,
                         user_args=[conn])
    urwid.connect_signal(create_screen.abort, 'click', on_abort_pressed,user_args = [conn])
    data_screen.main_panel.original_widget = urwid.WidgetPlaceholder(urwid.Padding(create_screen.top))

def on_abort_pressed(conn,button):
    data_screen.main_panel.original_widget = data_screen.view_panel
    data_screen.refresh_left_panel(databaseapi.showTables(conn), conn)
    data_screen.screen.set_focus(0)
if __name__ == "__main__":
    main()
