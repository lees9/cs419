#!/usr/bin/python

###  This just displays what you type in and outputs on screen


import urwid
import urwid.curses_display

class Screen:
    def __init__(self, tui):
        self.tui = tui

    def addLine(self, text):
        self.lines.append(urwid.Text(text))
        self.listbox.set_focus(len(self.lines) - 1)
        self.redisplay()

    def redisplay(self):
        canvas = self.frame.render(self.size, focus=True)
        self.tui.draw_screen(self.size, canvas)

    def run(self):
        self.size = self.tui.get_cols_rows()
        self.lines = [urwid.Text('TEXT')]
        self.listbox = urwid.ListBox(self.lines)
        self.input = urwid.Edit()

        self.frame = urwid.Frame(self.listbox, footer=self.input)
        self.frame.set_focus('footer')

        self.redisplay()

        while 1:
            keys = self.tui.get_input()

            for key in keys:
                if key == 'window resize':
                    self.size = self.tui.get_cols_rows()
                elif key == 'enter':
                    text = self.input.get_edit_text()
                    self.input.set_edit_text('')
                    self.addLine(text)
                elif key in ('up', 'down', 'page up', 'page down'):
                    self.listbox.keypress(self.size, key)
                else:
                    self.frame.keypress(self.size, key)

                self.redisplay()

if __name__ == '__main__':
    tui = urwid.curses_display.Screen()
    screen = Screen(tui)
    tui.run_wrapper(screen.run)