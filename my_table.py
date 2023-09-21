import tkinter as tk
import datetime
from tkinter import VERTICAL, ttk
import unicodedata
from unidecode import unidecode
import customtkinter
from ttkthemes import ThemedStyle


class CustomTreeview(ttk.Treeview):
    """This class is a custom Treeview widget that is used in the StudentsTable class."""

    def __init__(self, style: ttk.Style, *args, active_color="LightSteelBlue2", inactive_color="Salmon", **kwargs, ):
        self.style = style

        self.style.configure("MyTable.Treeview.Selected", foreground="white")

        super().__init__(*args, style="MyTable.Treeview", **kwargs)

        self.tag_configure("active", background=active_color)
        self.tag_configure("inactive", background=inactive_color)
        self.tag_configure('odd', background='#ADD8E6')
        self.tag_configure('even', background='#87CEEB')
        self.tag_configure('blank', background='white')

        self.tag_bind("active", "<<TreeviewSelect>>",
                      self.on_active_row_selected)
        self.tag_bind("inactive", "<<TreeviewSelect>>",
                      self.on_inactive_row_selected)
        self.tag_bind('odd', "<<TreeviewSelect>>", self.on_active_row_selected)
        self.tag_bind('even', "<<TreeviewSelect>>",
                      self.on_active_row_selected)
        self.previous_selection = None
        self.selected_student_row = None

    def on_active_row_selected(self, event):
        # pylint: disable=unused-argument
        """This method is called when the user selects an active row."""
        self.style.map("MyTable.Treeview", background=[
                       ("selected", "Blue")])

        if self.selection() == self.previous_selection:
            self.selection_remove(self.previous_selection)
            self.previous_selection = None
            self.selected_student_row = None
        elif self.selection() != self.previous_selection and self.selection():
            self.previous_selection = self.selection()
            selected_item = self.selection()
            self.selected_student_row = self.item(selected_item)["values"]

    def on_inactive_row_selected(self, event):
        # pylint: disable=unused-argument
        """This method is called when the user selects an inactive row."""
        self.style.map("MyTable.Treeview", background=[
            ("selected", "IndianRed4")])

        if self.selection() == self.previous_selection:
            self.selection_remove(self.previous_selection)
            self.previous_selection = None
            self.selected_student_row = None
        elif self.selection() != self.previous_selection and self.selection():
            self.previous_selection = self.selection()
            selected_item = self.selection()
            self.selected_student_row = self.item(selected_item)["values"]


class CustomTable(tk.Frame):

    def __init__(self,
                 master=None,
                 manager=None,
                 show_inactive=True,
                 font_name="Bahnschrift SemiLight",
                 font_size=16,
                 heading_names=("Name", "Referenced by",
                                "Address", "Telephone", "Comments"),
                 column_widths=(100, 100, 75, 75, 75),
                 column_types=("Name", "Name", "Name",
                               "Name", "Name"),
                 data_active_index=None,
                 active_color="LightSteelBlue2",
                 inactive_color="salmon"
                 ):

        if not (len(heading_names) == len(column_widths) and len(heading_names) == len(column_types)):
            raise ValueError(
                "The number of heading names must be equal to the number of column widths and column types.")

        super().__init__(master)
        self.master = master
        self.manager = manager
        self.right_click_commands = []
        self.double_click_command = []
        self.column_types = column_types
        self.show_inactive = show_inactive
        self.data_active_index = data_active_index
        self.style = ttk.Style()

        self.font_name = font_name
        self.font_size = font_size
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=(
            self.font_name, self.font_size))
        self.style.configure("Treeview", rowheight=int(self.font_size * 1.8))
        self.style.configure("Treeview.Heading", font=(
            self.font_name, self.font_size + 2))

        self.heading_names = heading_names
        self.column_widths = {}

        for index, column in enumerate(self.heading_names):
            self.column_widths.update({column: column_widths[index]})

        self.previous_col_index = None
        self.searchboxes_frame = None
        self.textboxes_frames = []
        self.table_frame = None

        self.SORT_ASCENDING = True

        self._create_frames()
        self._table_container = tk.Frame(self.table_frame)
        self._table_container.pack(fill='both', expand=True)
        self._create_table(active_color, inactive_color)
        self.selected_student_row = self.table.selected_student_row
        self._create_scrollbar()
        self.search_entry_widgets = []
        self._create_search_entries()

        self.data = []
        self.filtered_data = []
        self.sorted_data = []
        self.data_to_display = []
        self.displayed_data = []
        self._after_job = None

        # self.fill_table(show_inactive=self.show_inactive)
        self.table.bind("<Double-Button-1>", self.on_double_click)
        self.table.bind("<Button-3>", self.on_right_click)
        self.table.bind("<Configure>", self.update_textboxes)
        self.idx = 0

    # def change_theme(self):
    #     self.style.theme_use(self.themes[self.idx])
    #     self.theme_label.configure(text="Theme: " + self.themes[self.idx])
    #     self.idx += 1

    def disable_searchboxes(self):
        for widget in self.search_entry_widgets:
            widget.pack_forget()
            widget.destroy()
        for frame in self.textboxes_frames:
            frame.pack_forget()
            frame.destroy()

    def set_data(self, data, reset_scroll=True):

        self.data = data

        self.update_data(reset_scroll=reset_scroll)

    def update_data(self, reset_scroll):
        if self.data is None:
            self.data_to_display = []
            self.fill_table()
            return

        # Call self.filter_data only if the user has entered something in the search boxes
        if not all([self.search_entries[col].get() == "" for col in self.column_widths]):
            self.filter_data()  # This will update self.filtered_data
            if self.previous_col_index is not None:

                self.SORT_ASCENDING = not self.SORT_ASCENDING
                self.sort_and_display_data(
                    self.heading_names[self.previous_col_index], reset_scroll=reset_scroll)
            else:
                self.data_to_display = self.filtered_data
                self.fill_table(show_inactive=self.show_inactive)

        else:
            self.filtered_data = self.data
            # If the user hasn't entered anything in the search boxes,
            # then if the table is sorted, we need to sort it again
            if self.previous_col_index is not None:

                self.SORT_ASCENDING = not self.SORT_ASCENDING
                self.sort_and_display_data(
                    self.heading_names[self.previous_col_index], reset_scroll=reset_scroll)

            else:  # if the table is not sorted and the user hasn't entered anything in the search boxes, then we just need to display the data
                self.data_to_display = self.data

                self.fill_table(show_inactive=self.show_inactive)

    def _create_table(self, active_color, inactive_color):

        self.table = CustomTreeview(self.style, self._table_container, columns=[
                                    heading for heading in self.heading_names], active_color=active_color, inactive_color=inactive_color, show='headings', selectmode='browse')

        for heading in self.heading_names:
            # get column width from dictionary
            col_width = self.column_widths[heading]
            self.table.heading(heading, text=heading, anchor="center",
                               command=lambda col=heading: self.sort_and_display_data(col))

            self.table.column(heading,
                              width=col_width, anchor="center")

        self.table.pack(fill='both', expand=True, side='top')

    def _create_search_entries(self):
        self.search_entries = {}

        for i, col in enumerate(self.column_widths):
            self.search_entries[col] = tk.StringVar()
            self.search_entries[col].trace(
                "w", lambda *args, col=col: self.on_search_text_change())

            search_entry = tk.Entry(self.textboxes_frames[i], textvariable=self.search_entries[col], font=(
                self.font_name, self.font_size-2), justify='center')
            self.search_entry_widgets.append(search_entry)
            search_entry.pack(fill='both', side="left", expand=True)

    def _create_frames(self):

        self.searchboxes_frame = tk.Frame(self)
        self.searchboxes_frame.configure(height=30)
        self.searchboxes_frame.pack(fill='x', side='top')

        for i, key in enumerate(self.column_widths):
            self.textboxes_frames.append(
                tk.Frame(self.searchboxes_frame))
            self.textboxes_frames[i].configure(
                height=30, width=self.column_widths[key])

            self.textboxes_frames[i].pack(side='left')
            self.textboxes_frames[i].pack_propagate(0)  # !ΠΑΝΑΓΙΑ!

        self.table_frame = tk.Frame(self)
        self.table_frame.pack(expand=True, fill='both', side='top')

    def _create_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(
            self._table_container, orient=VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.table.pack(side='left', fill='both', expand=True)
        self.table.configure(yscrollcommand=self.scrollbar.set)

    def filter_data(self):
        query_list = [self.search_entries[col].get()
                      for col in self.column_widths]

        self.filtered_data = []

        for row in self.data:
            is_matching = True
            for i, query in enumerate(query_list):
                query = unidecode(query.lower())
                if query:
                    if query.startswith('<') or query.startswith('>'):
                        try:
                            num = float(query[1:])
                            if query.startswith('<') and float(row[i]) >= num:
                                is_matching = False
                                break
                            elif query.startswith('>') and float(row[i]) <= num:
                                is_matching = False
                                break
                        except ValueError:  # Occurs if the row item or query isn't a number
                            is_matching = False
                            break
                    elif query not in unidecode(row[i].lower()):
                        is_matching = False
                        break

            if is_matching:
                self.filtered_data.append(row)

        self.data_to_display = self.filtered_data

    def sort_and_display_data(self, column, reset_scroll=True):
        """Sorts the table by the column that was clicked"""
        # pylint: disable=unused-variable

        def strip_accents(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                           if unicodedata.category(c) != 'Mn')
        if reset_scroll:
            self.table.yview_moveto(0)  # moves the scrollbar to the top

        heading_names_dict = {heading: i for i,
                              heading in enumerate(self.heading_names)}

        col_index = heading_names_dict[column]

        if self.previous_col_index != None and self.previous_col_index != col_index:
            self.table.heading(
                self.previous_col_index, text=self.heading_names[self.previous_col_index])
        if self.previous_col_index == col_index:
            self.SORT_ASCENDING = not self.SORT_ASCENDING

        # sort the data based on the column clicked

        if self.SORT_ASCENDING:
            if self.column_types[col_index] == "Date":

                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: datetime.datetime.strptime(x[col_index]+x[col_index+1], '%d/%m/%Y%H:%M'))
            elif self.column_types[col_index] == "Date_dont_use_time":
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: datetime.datetime.strptime(x[col_index], '%d/%m/%Y'))
            elif self.column_types[col_index] == "Name":
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: strip_accents(x[col_index].split(" ")[1]) if len(x[col_index].split(" ")) > 1 else strip_accents(x[col_index].split(" ")[0]))

            else:
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: x[col_index])
            self.table.heading(
                column, text=self.heading_names[col_index] + ' \u25B2')

        else:
            if self.column_types[col_index] == "Date":

                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: datetime.datetime.strptime(
                                              x[col_index]+x[col_index+1], '%d/%m/%Y%H:%M'), reverse=True)
            elif self.column_types[col_index] == "Date_dont_use_time":
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: datetime.datetime.strptime(x[col_index], '%d/%m/%Y'), reverse=True)
            elif self.column_types[col_index] == "Name":
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: strip_accents(x[col_index].split(" ")[1]) if len(x[col_index].split(" ")) > 1 else strip_accents(x[col_index].split(" ")[0]), reverse=True)
            else:
                self.sorted_data = sorted(self.filtered_data,
                                          key=lambda x: x[col_index], reverse=True)
            self.table.heading(
                column, text=self.heading_names[col_index] + ' \u25BC')

        self.previous_col_index = col_index
        self.data_to_display = self.sorted_data
        self.fill_table(show_inactive=self.show_inactive)

    def set_mode(self, mode=None, this_widget=None):
        if type(mode) is not str and mode is not None:
            raise TypeError("mode must be a string")
        if mode is None:
            mode = customtkinter.get_appearance_mode()

        if this_widget is not None:
            if mode.upper() == "LIGHT":
                this_widget.configure(background="white")
            elif mode.upper() == "DARK":
                this_widget.configure(background="gray20")
            return
        if mode.upper() == "LIGHT":

            for widget in self.search_entry_widgets:

                widget.configure(background="white")

            self.table.tag_configure("active", background="LightSteelBlue2")
            self.table.tag_configure("inactive", background="salmon")
            self.table.style.configure("MyTable.Treeview", background="white",
                                       foreground="black", fieldbackground="white")
        elif mode.upper() == "DARK":
            for widget in self.search_entry_widgets:
                widget.configure(background="gray20")

            self.table.tag_configure("active", background="LightSteelBlue2")
            self.table.tag_configure("inactive", background="salmon")
            self.table.style.configure("MyTable.Treeview",
                                       background="gray20", foreground="black", fieldbackground="gray20")

    def on_search_text_change(self):
        for widget in self.search_entry_widgets:

            if widget.get() != "":
                if customtkinter.get_appearance_mode() == 'Light':

                    widget.configure(background="light green")

                elif customtkinter.get_appearance_mode() == 'Dark':
                    widget.configure(background="violet")
            else:
                self.set_mode(this_widget=widget)

        if self._after_job:
            self.after_cancel(self._after_job)
        self._after_job = self.after(
            50, lambda arg=True: self.update_data(reset_scroll=arg))

    def update_textboxes(self, event):
        # pylint: disable=unused-argument

        self.update()

        for i, col in enumerate(self.column_widths):
            self.column_widths[col] = self.table.column(col, "width")
            self.textboxes_frames[i].configure(
                width=self.column_widths[col])

    def fill_table(self, show_inactive=True):

        self.table.delete(*self.table.get_children())
        self.displayed_data = []
        for row in self.data_to_display:
            status = 'active' if self.data_active_index is None else 'inactive' if row[
                self.data_active_index] == '0' else 'active'
            if not show_inactive and status == 'inactive':
                continue
            self.table.insert('', 'end', values=row, tags=status)
            self.displayed_data.append(row)

    def manual_fill_table(self, data, show_inactive=True):
        self.table.delete(*self.table.get_children())
        self.displayed_data = []
        for row in data:

            status = 'active' if self.data_active_index is None else 'inactive' if row[
                self.data_active_index] == '0' else 'active'
            if not show_inactive and status == 'inactive':
                continue
            self.table.insert('', 'end', values=row, tags=status)
            self.displayed_data.append(row)
            # check if self.manager has an attribute called sum_label and if it does, update it
        if hasattr(self.manager, "sum_label"):

            self.manager.update_data(target="update_sum")

    def on_double_click(self, event):
        row_id = self.table.identify('row', event.x, event.y)
        if row_id:
            self.table.focus(row_id)
            self.right_click_commands[0][1](row_id)

    def donothing(self):
        pass

    def on_right_click(self, event):
        # we need to identify if one or multiple rows are selected

        row_id = self.table.identify('row', event.x, event.y)

        self.table.focus(row_id)

        if row_id:
            if row_id != self.table.previous_selection:
                self.table.selection_set(row_id)
                self.table.previous_selection = row_id
            context_menu = tk.Menu(self, tearoff=0)

            for i, command in enumerate(self.right_click_commands):

                if i == len(self.right_click_commands)-1:
                    context_menu.add_separator()
                    context_menu.add_command(
                        label=command[0], command=lambda cmd=command: cmd[1](row_id), font=('Bahnschrift SemiLight', 12))
                    break
                context_menu.add_command(
                    label=command[0], command=lambda cmd=command: cmd[1](row_id), font=('Bahnschrift SemiLight', 12))

            # Display the context menu
            context_menu.tk_popup(event.x_root, event.y_root)


if __name__ == "__main__":
    root = tk.Tk()
    table = CustomTable(root, data_active_index=4,
                        show_inactive=True)
    table.set_data([["Περπινιάδης", "Μαλάκας", "Χαλάνδρι", "698547596", "0"],
                   ["Τσιμπουκλής", "Σκατιάρης", "Χαλάνδρι", "698547596", "1"],
                   ["Χαζοβιόλης", "Πουτσογλύφτης",
                       "Χαλάνδρι", "698547596", "1"],
                   ["Πιπόζης", "Γαμημένος", "Χαλάνδρι", "698547596", "0"]
                    ])
    table.pack(fill='both', expand=True)
    root.mainloop()
