import urwid
import datetime
import mysql.connector
import loginbox
from urwid import Signals


conn = None
box = None
main_screen = None


def main():
    spacer = urwid.Divider()
    heading = urwid.Pile([('weight', 0, spacer)],focus_item=0)
    box = loginbox.LoginBox()
    main_screen = urwid.Filler(heading)
    urwid.connect_signal(box.login, 'click', box.on_login_pressed,user_args=[conn])
    heading.contents.append((box.top, ('given', 20)))
    heading.set_focus(1)
    urwid.connect_signal(box.exit, 'click', box.on_exit_pressed)
    loop = urwid.MainLoop(main_screen, pop_ups=True)
    loop.run()
    pass

if __name__ == "__main__":
    main()
