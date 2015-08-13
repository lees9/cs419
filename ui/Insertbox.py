import urwid
import databaseapi
import json

class Insertbox(urwid.WidgetWrap):
    signals = ['insert', 'failure', 'abort']
    text1 = urwid.Text("Table list:\n")
    div = urwid.Divider()
    text = urwid.Text(u"")
    table_name = urwid.Edit(u"Enter the name of the table to insert into:\n")
    _next = urwid.Button(u"Next")
    abort = urwid.Button(u"Back to main")
    status = urwid.Text(u"")
    iview = urwid.WidgetPlaceholder(urwid.Divider())
    pile = urwid.Pile([text1, text, div, table_name, div, _next, div, abort, div, status])
    insert_button = urwid.Button(u"Insert")
    back_button = urwid.Button(u"Back")
    status2 = urwid.Text(u"")
    status3 = urwid.Text(u"")
    top = urwid.Filler(pile, valign='top')
    def __init__(self):
        pass

    def next_view(self, conn, table_name):
        selected_table = self.table_name.get_edit_text()
        table_fields = databaseapi.showStructure(conn, selected_table)
        ins_status = urwid.Text(u"")
        insert_button = urwid.Button(u"Insert")
        if table_fields == -1:
            self.status.set_text("Invalid table. Please make sure the table entered is in the database")
        else:
            header = urwid.Text("Please enter for each field. If none use 'NULL'\n")
            input_pile = urwid.Pile([header])
            njstable_fields = json.loads(table_fields)
            table_field_names = []
            fields = []
            count = 0;
            for row in njstable_fields:
                fields.append(urwid.Edit(str(row[0])+" "+str(row[1])+"\n"))
                input_pile.contents.append((fields[count], input_pile.options()))
                table_field_names.append(row[0])
                count = count + 1
            input_pile.contents.append((self.div, input_pile.options()))
            input_pile.contents.append((self.back_button, input_pile.options()))
            input_pile.contents.append((self.insert_button, input_pile.options()))
            input_pile.contents.append((self.abort, input_pile.options()))
            input_pile.contents.append((self.div, input_pile.options()))
            input_pile.contents.append((self.status2, input_pile.options()))
            input_pile.contents.append((self.status3, input_pile.options()))
            result_view = urwid.Filler(input_pile)
            urwid.connect_signal(self.insert_button, 'click', self.insert_row, user_args=[selected_table, fields, table_field_names,
                                                                                          count, conn])
            self.top.original_widget = urwid.Padding(input_pile,('relative', 100), 'pack')
            input_pile.set_focus(1)
            
        
    def insert_row(self, selected_table, fields, table_field_names, count, conn, button):
        self.status2.set_text(u"Inserting to: " + selected_table)
        insert_input = []
        for row in fields:
            insert_input.append(row.get_edit_text())
        for i in range(0, len(insert_input)):
            if (len(insert_input[i]) == 0):
                insert_input[i] = "NULL"

        x = databaseapi.insert(conn, str(selected_table), insert_input)
        if (x == 0):
            self.status3.set_text(u"Insert successfuly")
        else:
            self.status3.set_text(u"Insert failed. Please check your inputs")
