"""This module contains the LessonsTable class which is used to display the lessons in a table."""

import datetime
import sqlite3
import tkinter as tk
import customtkinter
from tkinter import VERTICAL, ttk
from unidecode import unidecode

from student import Lesson, Student
# from student import Student, Lesson

# This is the index of the columns in the table.table data contains all these values.
# Not all of them are displayed though.
DATE = 0
TIME = 1
NAME = 2
PRICE = 3
PAID = 4
STUDENTS_ID = 5
ACTIVE = 6
UNIQUE_IDENTIFIER = 7


# LessonsCustomTreeview
class LessonsCustomTreeview(ttk.Treeview):
    """This class is a custom Treeview widget that is used in the LessonsTable class."""

    def __init__(self, style, *args, **kwargs):
        self.style = style

        self.style.configure("Lessons.Treeview", background="white",
                             foreground="black", fieldbackground="pink")

        super().__init__(*args, style="Lessons.Treeview", **kwargs)

        self.tag_configure("paid", background="LightSteelBlue2")
        self.tag_configure("unpaid", background="salmon")

        self.tag_bind("paid", "<<TreeviewSelect>>",
                      self.on_paid_row_selected)
        self.tag_bind("unpaid", "<<TreeviewSelect>>",
                      self.on_unpaid_row_selected)
        self.previous_selection = None
        self.selected_lesson = None

    def on_paid_row_selected(self, event):
        # pylint: disable=unused-argument
        """This method is called when the user selects a paid lesson."""
        self.style.map("Lessons.Treeview",
                       background=[('selected', 'Blue')])

        if self.selection() == self.previous_selection:
            self.selection_remove(self.previous_selection)
            self.previous_selection = None
            self.selected_lesson = None
        elif self.selection() != self.previous_selection and self.selection():
            self.previous_selection = self.selection()
            selected_item = self.selection()
            self.selected_lesson = self.item(selected_item)["values"]

    def on_unpaid_row_selected(self, event):
        # pylint: disable=unused-argument
        """This method is called when the user selects an unpaid lesson."""
        self.style.map("Lessons.Treeview",
                       background=[('selected', 'IndianRed4')])

        if self.selection() == self.previous_selection:
            self.selection_remove(self.previous_selection)
            self.previous_selection = None
            self.selected_lesson = None
        elif self.selection() != self.previous_selection and self.selection():
            self.previous_selection = self.selection()
            selected_item = self.selection()
            self.selected_lesson = self.item(selected_item)["values"]


class LessonsDatabase:
    @staticmethod
    def fetch_data():

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT Datetime,Datetime,Student,Price,Paid,Lessons_ID,Active,Unique_Identifier FROM Lessons''')
        rows = cursor.fetchall()

        conn.close()
        list_of_strings = [[str(e) for e in row] for row in rows]

        for row in list_of_strings:
            row[DATE] = datetime.datetime.strptime(
                row[DATE], "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
            row[TIME] = datetime.datetime.strptime(
                row[TIME], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
            if row[TIME] == "00:00":
                row[TIME] = "-"

        return list_of_strings

    @staticmethod
    def delete_lesson(lesson_obj):

        conn = []
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            query = "DELETE FROM Lessons WHERE (Student,Datetime) = (?,?)"
            cursor.execute(query, (lesson_obj.name, lesson_obj.date_time))
            conn.commit()
        finally:
            if conn:

                conn.close()

    @staticmethod
    def update_lesson(lesson_obj_old, lesson_obj_new):
        conn = None
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            query = "UPDATE Lessons SET Student=?, Datetime=?, Paid=? WHERE Student=? AND Datetime=?"
            cursor.execute(query, (lesson_obj_new.name, lesson_obj_new.date_time,
                           lesson_obj_new.paid, lesson_obj_old.name, lesson_obj_old.date_time))
            conn.commit()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def return_lesson_object_from_database(unique_identifier):
        """Returns a lesson object from the database based on its unique identifier"""
        conn = None
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            # Insert the student's information into the database
            query = '''SELECT Student,Datetime,Price,Paid FROM lessons WHERE "Unique_Identifier" = ?'''
            cursor.execute(query, (unique_identifier,))
            lesson = cursor.fetchone()
            conn.close()
            return Lesson(Student(name=lesson[0]), date_time=lesson[1], price=lesson[2], paid=lesson[3], unique_identifier=unique_identifier)
        finally:
            if conn:
                conn.close()


class LessonsTable(tk.Frame):
    def __init__(self, master, lessons_management, inactive=False, takefocus=True):
        super().__init__(master)
        self.master = master
        self.lessons_management = lessons_management
        self.takefocus = takefocus
        self.style = ttk.Style()
        self.font_size = 15
        self.style.configure("Treeview", font=(
            "Bahnschrift SemiLight", self.font_size))
        self.style.configure("Treeview", rowheight=int(self.font_size * 1.8))
        self.style.configure("Treeview.Heading", font=(
            "Bahnschrift SemiLight Bold", self.font_size + 2))

        self.column_widths = {"Date": 120,
                              "Time": 120,
                              "Name": 270,
                              "Price": 80,
                              "Paid": 80,
                              }

        self.heading_names = [
            ["Date", "Ημ/νία"],
            ["Time", "Ώρα"],
            ["Name", "Όνομα"],
            ["Price", "Τιμή"],
            ["Paid", "Paid"]
        ]
        self.previous_col_index = None
        self.searchboxes_frame = None
        self.textboxes_frames = []
        self.table_frame = None

        self.filtered_data = []
        self.SORT_ASCENDING = True
        self.show_inactive = inactive
        self.inactive_students = []
        self.create_frames()
        self.table_container = tk.Frame(self.table_frame)

        self.table_container.pack(fill='both', expand=True)

        self.create_table()
        self.create_scrollbar()
        self.create_search_entries()

        self.data = LessonsDatabase.fetch_data()
        self.final_data = self.data
        self.displayed_data = []

        self.filter_data()
        # This trick will sort the table by date when the program starts
        self.previous_col_index = DATE
        self.on_header_click(self.heading_names[DATE][0])
        # now lets bind a right click to the table
        self.context_menu = tk.Menu(self, tearoff=0)

        self.table.bind("<Button-3>", self.on_right_click)
        self.table.bind("<Configure>", self.update_textboxes)
        # self.table.bind(
        #    "<Double-1>", self.master.master.on_student_double_click)
        # self.table.bind("<Down>", self.on_down_arrow_key)

    # def on_down_arrow_key(self, event):
    #     # pylint: disable=unused-argument
    #     """Selects the first row when not in focus ??? the down arrow key is pressed"""
    #     if self.table.focus_displayof() != self.table:  # focus_displayof() returns the widget that has the focus
    #         # if not self.table.selection():
    #         first_row = self.table.get_children()[0]
    #         self.table.selection_set(first_row)
    #         self.table.focus_set()
    #         self.table.focus(first_row)

    def create_table(self):

        self.table = LessonsCustomTreeview(self.style, self.table_container, columns=(
            "Date", "Time", "Name", "Price", "Paid"), show='headings')
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
            search_entry.configure(takefocus=self.takefocus)

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
        self.table.yview_moveto(0)  # moves the scrollbar to the top
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

        self.final_data = self.filtered_data
        self.fill_table(show_inactive=self.show_inactive)

        if self.previous_col_index != None:
            self.table.heading(
                self.previous_col_index, text=self.heading_names[self.previous_col_index][1])

    def on_right_click(self, event):
        row_id = self.table.identify('row', event.x, event.y)
        self.table.focus(row_id)

        if row_id:
            if row_id != self.table.previous_selection:
                self.table.selection_set(row_id)
                self.table.previous_selection = row_id

            # Create the context menu
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(
                label="Επεξεργασία", command=lambda: self.edit_lesson(row_id))

            context_menu.add_command(
                label="Έχει πληρωθεί", command=lambda: self.set_paid_true(row_id))
            context_menu.add_command(label="Δεν έχει πληρωθεί", command=lambda: self.set_paid_false(row_id,)
                                     )
            context_menu.add_separator()
            context_menu.add_command(
                label="Διαγραφή", command=lambda: self.delete_lesson(row_id))

            # Display the context menu
            context_menu.tk_popup(event.x_root, event.y_root)

    def set_paid_true(self, row_id):

        this_lesson = LessonsDatabase.return_lesson_object_from_database(
            unique_identifier=self.table.item(row_id)['values'][UNIQUE_IDENTIFIER])
        this_lesson.set_paid(True)
        self.update_data()

    def set_paid_false(self, row_id):

        this_lesson = LessonsDatabase.return_lesson_object_from_database(
            unique_identifier=self.table.item(row_id)['values'][UNIQUE_IDENTIFIER])
        this_lesson.set_paid(False)
        self.update_data()

    def edit_lesson(self, row_id):
        """This method is called when the user selects the 'Επεξεργασία' option from the context menu."""
        # Add the implementation for editing a lesson here
        this_student = Student(name=self.table.item(row_id)['values'][2])
        old_lesson = Lesson(
            this_student, f"{self.table.item(row_id)['values'][0]} {self.table.item(row_id)['values'][1]}", paid=1 if self.table.item(row_id)['values'][3] == "Ναι" else 0,
            date_time_format="HUMAN")
        self.lessons_management.new_lesson_gui.set_lesson_entry(old_lesson)

    def delete_lesson(self, row_id):
        """This method is called when the user selects the 'Διαγραφή' option from the context menu."""
        # Add the implementation for deleting a lesson here
        # The row_id variable contains the id of the row that the user right clicked on
        # Use this row to get the lesson datetime and name, and then delete the lesson from the database

        date = self.table.item(row_id)['values'][0]
        time = self.table.item(row_id)['values'][1]
        name = self.table.item(row_id)['values'][2]
        this_student = Student(name=name)
        if time == "-":
            time = "00:00"

        this_lesson = Lesson(
            this_student, f"{date} {time}", date_time_format="HUMAN")
        # now we create a tktop level window to ask the user if he is sure he wants to delete the lesson
        delete_lesson_window = customtkinter.CTkToplevel(self)
        delete_lesson_window.title("Διαγραφή Μαθήματος")
        screen_width = delete_lesson_window.winfo_screenwidth()
        screen_height = delete_lesson_window.winfo_screenheight()
        window_width = 450
        window_height = 200
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        delete_lesson_window.geometry("%dx%d+%d+%d" %
                                      (window_width, window_height, x_coord, y_coord))
        delete_lesson_window.resizable(False, False)
        delete_lesson_window.grab_set()
        delete_lesson_window.focus_set()
        user_input = tk.BooleanVar()
        user_input.set(False)

        def on_yes():
            user_input.set(True)
            delete_lesson_window.destroy()

        def on_no():
            user_input.set(False)
            delete_lesson_window.destroy()
        delete_lesson_window.protocol(
            "WM_DELETE_WINDOW", delete_lesson_window.destroy)
        yes_button = customtkinter.CTkButton(delete_lesson_window,
                                             text="Ναι", width=100, height=50, command=on_yes)
        no_button = customtkinter.CTkButton(delete_lesson_window,
                                            text="Όχι", width=100, height=50, command=on_no)

        label = customtkinter.CTkLabel(
            delete_lesson_window, text=f"Διαγραφή του μαθήματος του μαθητή {name} στις {date} {time};", font=("Bahnschrift SemiLight Bold", 16), wraplength=280)
        label.pack(side="top", padx=10, pady=10)
        yes_button.pack(side="left", padx=30, pady=10)
        no_button.pack(side="right", padx=30, pady=10)
        delete_lesson_window.wait_window(delete_lesson_window)

        if user_input.get():
            LessonsDatabase.delete_lesson(this_lesson)
            self.update_data()
        else:
            return

    def on_header_click(self, column):
        self.table.yview_moveto(0)  # moves the scrollbar to the top
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
            if col_index == DATE:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: datetime.datetime.strptime(f"{x[DATE]} {x[TIME] if x[TIME] != '-' else '00:00'}", '%d/%m/%Y %H:%M'))
            elif col_index == NAME:

                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index].split(" ")[1] if len(x[col_index].split(" ")) > 1 else x[col_index].split(" ")[0])

            else:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index])
            self.table.heading(
                column, text=self.heading_names[col_index][1] + ' \u25B2')

        else:
            if col_index == DATE:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: datetime.datetime.strptime(f"{x[DATE]} {x[TIME] if x[TIME] != '-' else '00:00'}", '%d/%m/%Y %H:%M'), reverse=True)
            elif col_index == NAME:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index].split(" ")[1] if len(x[col_index].split(" ")) > 1 else x[col_index].split(" ")[0], reverse=True)
            else:
                sorted_data = sorted(self.filtered_data,
                                     key=lambda x: x[col_index], reverse=True)
            self.table.heading(
                column, text=self.heading_names[col_index][1] + ' \u25BC')

        # update the table with the sorted data
        self.final_data = sorted_data
        self.fill_table(show_inactive=self.show_inactive)

        self.previous_col_index = col_index

    def on_search_text_change(self):

        self.filter_data()
        if self.previous_col_index != None:
            self.SORT_ASCENDING = not self.SORT_ASCENDING
            self.on_header_click(
                self.heading_names[self.previous_col_index][0])

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
        self.data = LessonsDatabase.fetch_data()

        # Now we need to know if the data displayed is sorted. If it is, we need to sort the new data
        # and display it. If it isn't, we just need to display the new data

        if self.previous_col_index != None:
            self.SORT_ASCENDING = not self.SORT_ASCENDING
            self.filter_data()
            self.on_header_click(
                self.heading_names[self.previous_col_index][0])
        else:
            self.final_data = self.data
            self.fill_table(show_inactive=self.show_inactive)

        # self.filter_data()
        # self.on_header_click("Date")

    def fill_table(self, show_inactive=True):

        self.table.delete(*self.table.get_children())
        self.displayed_data = []
        for row in self.final_data:
            if row[ACTIVE] == "0" and not show_inactive:
                continue
            status = 'paid' if row[PAID] == '1' else 'unpaid'

            self.table.insert('', 'end', values=row, tags=status)
            self.displayed_data.append(row)

        if hasattr(self.lessons_management, 'lessons_table'):

            self.lessons_management.update_data(source=type(self))


if __name__ == "__main__":
    root = tk.Tk()
    table = LessonsTable(root, lessons_management=None)

    table.pack(fill='both', expand=True)
    root.mainloop()
