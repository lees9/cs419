import urwid
import databaseapi
import main
import json

class Deletescreen(urwid.WidgetWrap):
    signals = ['delete', 'failure', 'abort']
    text1 = urwid.Text("Table list:\n")
    div = urwid.Divider()
    text = urwid.Text(u"")
    table_name = urwid.Edit(u"Enter the name of the table to delete from:\n")
    _next = urwid.Button(u"Next")
    abort = urwid.Button(u"Back to main")
    status = urwid.Text(u"")
    iview = urwid.WidgetPlaceholder(urwid.Divider())
    pile = urwid.Pile([text1, text, div, table_name, div, _next, div, abort, div, status])
    delete_button = urwid.Button(u"Delete")
    back_button = urwid.Button(u"Back")
    text2 = urwid.Text(u"")
    status2 = urwid.Text(u"")
    status3 = urwid.Text(u"")
    top = urwid.Filler(pile, valign='top')
    def __init__(self):
        pass

    def next_view(self, conn, table_name):
        selected_table = self.table_name.get_edit_text()
        table_fields = databaseapi.showStructure(conn, selected_table)
        table_data = databaseapi.show_all(conn, selected_table)
        ins_status = urwid.Text(u"")
        if table_data == -1:
            self.status.set_text("Invalid table. Please make sure the table entered is in the database")
        else:
            header = urwid.Text("Please enter the Id# you would like to delete.")
            input_pile = urwid.Pile([header])
            njstable_fields = json.loads(table_fields)
            field_count = 0
            for row in njstable_fields:
                self.text2.set_text(self.text2.get_text()[0]+" "+str(row[0]))
            self.text2.set_text(self.text2.get_text()[0]+"\n")
            
            njstable_data = json.loads(table_data)
            data_fields = [] #urwid
            data_field_names = []
            data_count = 0

            for row in njstable_data:
                for col in row:
                    self.text2.set_text(self.text2.get_text()[0]+" "+str(col))
                self.text2.set_text(self.text2.get_text()[0]+"\n")
            input_pile.contents.append((self.text2, input_pile.options()))
            
            id_num = urwid.Edit("Id #: ")
            input_pile.contents.append((id_num, input_pile.options()))
            input_pile.contents.append((self.div, input_pile.options()))
            input_pile.contents.append((self.back_button, input_pile.options()))
            input_pile.contents.append((self.delete_button, input_pile.options()))
            input_pile.contents.append((self.abort, input_pile.options()))
            input_pile.contents.append((self.div, input_pile.options()))
            input_pile.contents.append((self.status2, input_pile.options()))
            input_pile.contents.append((self.status3, input_pile.options()))
            result_view = urwid.Filler(input_pile)
            urwid.connect_signal(self.delete_button, 'click', self.delete, user_args=[selected_table, id_num, conn])
            self.top.original_widget = urwid.Padding(input_pile,('relative', 100), 'pack')
            input_pile.set_focus(1)

    def delete(self, selected_table, id_num, conn, button):
        id_val = id_num.get_edit_text()
        x = databaseapi.delete(conn, selected_table, id_val)
        if (x == 0):
            self.status3.set_text(u"Row deleted successfully")
        else:
            self.status3.set_text(u"Delete failed. Please check the id input")
            
