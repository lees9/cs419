import urwid
import threading
import time

### Prints what is in the queue on loop, right now set up to print from DisplayTest class
### Not sure if this would work for a view window?
class Window:

    def __init__(self):
        self.listed = urwid.SimpleListWalker([])
        self.body = urwid.ListBox(self.listed)
        self.view = urwid.Frame(
            urwid.AttrWrap(self.body, 'body'))
        self.loop = urwid.MainLoop(self.view)
        self.print_out = DisplayTest()

    def start(self):
        threading1 = threading.Thread(target = self.fill_screen)
        threading1.daemon = True
        threading2 = threading.Thread(target = self.print_out.fill_queue)
        threading2.daemon = True
        threading1.start()
        threading2.start()
        self.loop.run()

    def fill_screen(self):  
        while True:
            if self.print_out.queue:
                self.listed.append(urwid.Text(('body', self.print_out.queue.pop(0))))
                try:
                    self.loop.draw_screen()
                    self.body.set_focus(len(self.listed)-1, 'above')
                except AssertionError: pass

    def to_screen(self, text):
        self.queue.append(text)


class DisplayTest:
    def __init__(self):
        self.message = 'Test print statement'
        self.queue = []

    def fill_queue(self):
        while 1:
            self.queue.append(self.message)
            time.sleep(2)

if __name__ == '__main__':
    i = Window()
    i.start()