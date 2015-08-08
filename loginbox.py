import urwid
import mysql.connector
from mysql.connector import errorcode

class LoginPopupLauncher(urwid.PopUpLauncher):

    def __init__(self, original_widget):
        urwid.PopUpLauncher.__init__(self, original_widget)

    def create_pop_up(self):
        pop_up = SuccessPopup()
        urwid.connect_signal(pop_up, 'close', lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left': 0, 'top': 1, 'overlay_width': 32, 'overlay_height': 14}


class SuccessPopup(urwid.WidgetWrap):
    signals = ['close']

    def __init__(self):
        response = urwid.Text(u"Successfully connected to database!")
        okay = urwid.Button(u"Ok")
        urwid.connect_signal(okay, 'click', lambda button: self._emit("close"))
        pile = urwid.Pile([response, okay])
        fill = urwid.Filler(pile)
        self.__super.__init__(fill)


class LoginBox(urwid.WidgetWrap):
    signals = ['success', 'failure']
    username  urwid.Edit("What is your username?\n", u"")
    password = urwid.Edit("What is your password?\n", u"", mask=u'*')
    database = urwid.Edit("What database? \n", u"")
    div = urwid.Divider()
    login = urwid.Button(u"Login")
    exit = urwid.Button(u"Exit")
    div2 = urwid.Divider()
    status = urwid.Text(u"")
    launcher = LoginPopupLauncher(status)
    pile = urwid.Pile([username, password, database, div, login, exit, div2, status])
    top = urwid.Filler(pile,valign='top')

    def __init__(self):
        pass


    def on_login_pressed(self, button, conn):
        self.launcher.open_pop_up()
        if not self.username or not self.password or not self.database:
            self.status.set_text("You must use a valid username, password, and database name.")
        else:
            try:
                conn = mysql.connector.connect(host="localhost",user=self.username.get_edit_text(),
                passwd=self.password.get_edit_text(),db=self.database.get_edit_text(),port=3307)
                self.launcher.open_pop_up()
                self.status.set_text("Successfully connected to database {0} as {1}".format(self.database.get_edit_text(),
                    self.username.get_edit_text()))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.status.set_text("You are not authorized to connect to the {0} database.".format(self.database.get_edit_text()))
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.status.set_text("{0} database does not exist on this SQL server!".format(self.database.get_edit_text()))
                else:self.status.set_text("Cannot connect to database, {0} as {1}".format(self.database.get_edit_text(),
                    self.username.get_edit_text()))

    def on_exit_pressed(self,button):
        raise urwid.ExitMainLoop()


