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
    data_screen.refresh_left_panel(databaseapi.showTables(conn),conn)
    tables = json.loads(databaseapi.showTables(conn))
    cols = databaseapi.showStructure(conn,tables[0])
    for col in cols:
        data_screen.data_panel.text.set_text(data_screen.data_panel.text.get_text()[0]+" "+str(col))
    data_screen.data_panel.text.set_text(databaseapi.showStructure(conn, tables[0]))
    popup_launcher.original_widget = urwid.WidgetPlaceholder(urwid.Filler(data_screen.screen))
    urwid.connect_signal(data_screen.logout, 'click', data_screen.on_logout_pressed)
    urwid.connect_signal(data_screen.insert,'click', on_create_table)


def on_login_failure(args):
    #TODO: Message for GTFO
    pass

def on_create_table():
    popup_launcher.original_widget=create_screen


if __name__ == "__main__":
    main()
