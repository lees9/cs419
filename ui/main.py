import urwid
import databaseapi
import datascreen
import loginbox
from loginbox import LoginPopupLauncher

conn = None
main_screen = None
popup_launcher = None
spacer = urwid.Divider()
heading = urwid.Pile([('weight', 1, spacer)], focus_item=0)
box = loginbox.LoginBox()
main_screen = urwid.Filler(heading)
data_screen = datascreen.Datascreen()
popup_launcher = LoginPopupLauncher(main_screen)
def main():
    urwid.connect_signal(box.login, 'click', box.on_login_pressed, user_args=[conn])
    urwid.connect_signal(box, 'success', on_login_success)
    heading.contents.append((box.top, ('given', 20)))
    heading.set_focus(1)
    urwid.connect_signal(box.exit, 'click', box.on_exit_pressed)
    loop = urwid.MainLoop(popup_launcher, pop_ups=True)
    loop.run()


def on_login_success(object,conn):
    data_screen.refresh_left_panel(databaseapi.showTables(conn))
    heading.contents = [(urwid.Filler(data_screen.screen),('given', 60))]
    tables_list = open('tables.txt', 'w')
    tables_list.writelines(databaseapi.showTables(conn))
    urwid.connect_signal(data_screen.logout, 'click', data_screen.on_logout_pressed)
    #popup_launcher.open_pop_up()


def on_login_failure(args):
    pass

if __name__ == "__main__":
    main()
