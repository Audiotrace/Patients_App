"""This module contains the PatientsTable class which is used to display the patients in a table."""

import datetime
import sqlite3
import tkinter as tk
from tkinter import VERTICAL, ttk
from unidecode import unidecode
from collections import Counter


class CustomTreeview(ttk.Treeview):
    """This class is a custom Treeview widget that is used in the PatientsTable class."""

    def __init__(self, style, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = style

        self.style.configure("Treeview", background="white",
                             foreground="black", fieldbackground="pink")

        self.tag_configure("active", background="thistle")
        self.tag_configure("inactive", background="salmon")

        self.tag_bind("active", "<<TreeviewSelect>>",
                      self.on_active_row_selected)
        self.tag_bind("inactive", "<<TreeviewSelect>>",
                      self.on_inactive_row_selected)

    def on_active_row_selected(self, event):
        """This method is called when the user selects an active patient."""
        # pylint: disable=unused-argument
        self.style.map("Treeview", background=[('selected', 'medium blue')])

    def on_inactive_row_selected(self, event):
        """This method is called when the user selects an inactive patient."""
        # pylint: disable=unused-argument
        self.style.map("Treeview", background=[('selected', 'pink')])


class PatientsDatabase:
    @staticmethod
    def fetch_data():
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Name, Age, Telephone, Profession,"Referenced By", Price, "Start Date", Active,ID FROM patients')
        rows = cursor.fetchall()

        conn.close()
        list_of_strings = [[str(e) for e in row] for row in rows]

        return list_of_strings

    @staticmethod
    def count_stats():
        data = PatientsDatabase.fetch_data()
        active_count = 0
        inactive_count = 0
        total_age = 0
        total_price = 0

        referencer_counter = Counter()

        for row in data:
            if row[7] == "1":
                active_count += 1
            else:
                inactive_count += 1

            total_age += int(row[1])
            total_price += float(row[5])
            referencer_counter[row[4]] += 1

        total_count = active_count + inactive_count
        mean_age = total_age / total_count if total_count > 0 else 0
        mean_price = total_price / total_count if total_count > 0 else 0
        most_frequent_referencer = referencer_counter.most_common(
            1)[0] if referencer_counter else ("", 0)

        return {
            "active_count": active_count,
            "inactive_count": inactive_count,
            "total_count": total_count,
            "mean_age": mean_age,
            "mean_price": mean_price,
            "most_frequent_referencer": most_frequent_referencer
        }


class PatientsTable(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.style = ttk.Style()
        self.font_size = 15
        self.style.configure("Treeview", font=(
            "Bahnschrift SemiLight", self.font_size))
        self.style.configure("Treeview", rowheight=int(self.font_size * 1.8))
        self.style.configure("Treeview.Heading", font=(
            "Bahnschrift SemiLight Bold", self.font_size + 2))

        self.column_widths = {"Name": 250, "Age": 80, "Telephone": 160,
                              "Profession": 300,
                              "Referenced By": 250,
                              "Price": 80, "start_date": 220}
        self.heading_names = [
            ["Name", "Όνομα"],
            ["Age", "Ηλικία"],
            ["Telephone", "Τηλ"],
            ["Profession", "Επάγγελμα"],
            ["Referenced By", "Προέλευση"],
            ["Price", "Τιμή"],
            ["start_date", "Ημερομηνία Έναρξης"]
        ]
        self.previous_col_index = None
        self.searchboxes_frame = None
        self.textboxes_frames = []
        self.table_frame = None

        self.filtered_data = []
        self.SORT_ASCENDING = True
        self.show_inactive = True
        self.create_frames()
        self.table_container = tk.Frame(self.table_frame)
        self.table_container.pack(fill='both', expand=True)
        self.create_table()
        self.create_scrollbar()
        self.create_search_entries()

        self.data = PatientsDatabase.fetch_data()
        self.data_to_display = self.data

        self.filter_data()

        self.table.bind(
            "<Double-1>", self.master.master.on_patient_double_click)
        self.master.master.bind("<Down>", self.on_down_arrow_key)

    def on_down_arrow_key(self, event):
        # pylint: disable=unused-argument
        """Selects the first row when not in focus ??? the down arrow key is pressed"""

        if not self.table.selection():
            first_row = self.table.get_children()[0]
            self.table.selection_set(first_row)
            self.table.focus_set()
            self.table.focus(first_row)

    def create_table(self):

        self.table = CustomTreeview(self.style, self.table_container, columns=("Name", "Age", "Telephone",
                                                                               "Profession", "Referenced By", "Price", "start_date"), show='headings')
        for heading in self.heading_names:
            # get column width from dictionary
            col_width = self.column_widths[heading[0]]
            self.table.heading(heading[0], text=heading[1], anchor="center",
                               command=lambda col=heading[0]: self.on_header_click(col))

            self.table.column(heading[0], width=col_width, anchor="center")

        self.table.pack(fill='both', expand=True, side='top')

    def create_search_entries(self):
        self.search_entries = {}

        for i, col in enumerate(self.column_widths):
            self.search_entries[col] = tk.StringVar()
            self.search_entries[col].trace(
                "w", lambda *args, col=col: self.on_search_text_change())

            search_entry = tk.Entry(self.textboxes_frames[i], textvariable=self.search_entries[col], font=(
                "Bahnschrift SemiLight", 12), justify='center')

            search_entry.pack(fill='both', side="left", expand=True)

    def create_frames(self):

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

    def create_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(
            self.table_container, orient=VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.table.pack(side='left', fill='both', expand=True)
        self.table.configure(yscrollcommand=self.scrollbar.set)

    def filter_data(self):
        query_list = [self.search_entries[col].get()
                      for col in self.column_widths]
        query_list = [unidecode(query.lower()) for query in query_list]
        # if query_list == [""]*len(query_list):
        #     self.sort_by_active_status()
        #     self.filtered_data = self.data
        #     return
        self.filtered_data = []

        for row in self.data:
            is_matching = True
            for i, query in enumerate(query_list):
                if query and query not in unidecode(row[i].lower()):
                    is_matching = False
                    break

            if is_matching:

                self.filtered_data.append(row)

        self.data_to_display = self.filtered_data
        self.fill_table(show_inactive=self.show_inactive)

        if self.previous_col_index != None:
            self.table.heading(
                self.previous_col_index, text=self.heading_names[self.previous_col_index][1])

    def on_header_click(self, column):

        # get the index of the column in the heading_names list

        heading_names_dict = {heading[0]: i for i,
                              heading in enumerate(self.heading_names)}

        col_index = heading_names_dict[column]

        if self.previous_col_index != None and self.previous_col_index != col_index:
            self.table.heading(
                self.previous_col_index, text=self.heading_names[self.previous_col_index][1])
        if self.previous_col_index == col_index:
            self.SORT_ASCENDING = not self.SORT_ASCENDING
        else:
            self.SORT_ASCENDING = True
        # sort the data based on the column clicked
        if self.SORT_ASCENDING:
            if col_index == 6:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: datetime.datetime.strptime(x[col_index], '%d/%m/%Y'))
            elif col_index == 0 or col_index == 4:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index].split(" ")[1] if len(x[col_index].split(" ")) > 1 else x[col_index].split(" ")[0])

            else:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index])
            self.table.heading(
                column, text=self.heading_names[col_index][1] + ' \u25B2')

        else:
            if col_index == 6:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: datetime.datetime.strptime(x[col_index], '%d/%m/%Y'), reverse=True)
            elif col_index == 0 or col_index == 4:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index].split(" ")[1] if len(x[col_index].split(" ")) > 1 else x[col_index].split(" ")[0], reverse=True)
            else:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index], reverse=True)
            self.table.heading(
                column, text=self.heading_names[col_index][1] + ' \u25BC')

        # update the table with the sorted data
        self.data_to_display = sorted_data
        self.fill_table(show_inactive=self.show_inactive)

        self.previous_col_index = col_index

    def on_search_text_change(self):
        self.filter_data()

    def update_textboxes(self, event):
        # pylint: disable=unused-argument

        # self.master.update_idletasks()
        # self.update_idletasks()
        self.update()

        for i, col in enumerate(self.column_widths):
            self.column_widths[col] = self.table.column(col, "width")
            self.textboxes_frames[i].configure(
                width=self.column_widths[col])

    def update_data(self):
        self.data = PatientsDatabase.fetch_data()
        # print("data updated")
        self.filter_data()

    def fill_table(self, show_inactive=True):
        self.table.delete(*self.table.get_children())
        for row in self.data_to_display:
            status = 'active' if row[7] == '1' else 'inactive'
            if not show_inactive and status == 'inactive':
                continue
            self.table.insert('', 'end', values=row, tags=status)


if __name__ == "__main__":
    root = tk.Tk()
    table = PatientsTable(root)
    print(table.heading_names)
    table.pack(fill='both', expand=True)
    root.mainloop()
