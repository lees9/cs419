import urwid
import datetime
import mysql.connector

conn = None
class SuccessPopup(urwid.WidgetWrap):
    signals = ['close']
    def __init__(self):
        response = urwid.Text(u"Successfully connected to database!")
        okay = urwid.Button(u"Ok")
        urwid.connect_signal(okay,'click',lambda button:self._emit("close"))
        pile = urwid.Pile([response,okay])
        fill = urwid.Filler(pile)
        self.__super.__init__(fill)


class LoginPopupLauncher(urwid.PopUpLauncher):
    def __init__(self,original_widget):
        urwid.PopUpLauncher.__init__(self,original_widget)

    def create_pop_up(self):
        pop_up = SuccessPopup()
        urwid.connect_signal(pop_up,'close',lambda button:self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0,'top':1,'overlay_width':32,'overlay_height':14}


class LoginBox(urwid.WidgetWrap):
    signals = ['success','failure']
    username = urwid.Edit("What is your username?\n",u"")
    password = urwid.Edit("What is your password?\n",u"",mask=u'*')
    database = urwid.Edit("What database? \n",u"")
    div = urwid.Divider()
    login = urwid.Button(u"Login")
    exit = urwid.Button(u"Exit")
    div2 = urwid.Divider()
    status = urwid.Text(u"")
    pile = urwid.Pile([username,password,database,div,login,exit,div2,status])
    top = urwid.Filler(pile,valign='top')

    def __init__(self):
        pass
    def on_login_pressed(self,button):
        if not self.username or not self.password or not self.database:

            pass #TODO: Add error popup
        else:
            conn = mysql.connector.connect(host="localhost",user=self.username.get_edit_text(),
                passwd=self.password.get_edit_text(),db=self.database.get_edit_text(),port=3306)
            if conn:
                self.status.set_text("Successfully connected to database {0} as {1}".format(self.database.get_edit_text(),
                    self.username.get_edit_text()))
            else:
                #TODO: print failure case!
                self.status.set_text("Cannot connect to database, {0} as {1}".format(self.database.get_edit_text(),
                    self.username.get_edit_text()))

    def on_exit_pressed(self,button):
        raise urwid.ExitMainLoop()

def main():
    box = LoginBox()
    main = urwid.Filler(box)
    urwid.connect_signal(box.login,'click',box.on_login_pressed)
    urwid.connect_signal(box.exit,'click',box.on_exit_pressed)
    loop = urwid.MainLoop(box.top, pop_ups=True)
    loop.run()


if __name__ == "__main__":
    main()