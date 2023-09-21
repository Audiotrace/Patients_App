'''A module containing all the tables used in the patients management application.'''

import time
import tkinter as tk
import customtkinter
import pytz
from datetime import datetime
from my_table import CustomTable
from tdamourakis_ctkinter import MessageBox

from patients_management_database import SessionsDatabase, GeneralDatabase
from edit_patient_gui import EditPatientGUI
from new_patient_gui import NewPatientGUI
from new_session_gui import NewSessionGUI
from patient import Patient
from session import Session


class PatientsTable(CustomTable):
    ''' Table for patients'''

    def __init__(self, master, manager=None):
        self.manager = manager
        super().__init__(master, manager, heading_names=("Ονοματεπώνυμο", "Ηλικία",
                                                         "Τηλέφωνο", "Επάγγελμα", "Προέλευση", "Τιμή", "Έναρξη"),
                         column_widths=("220", "10", "80", "250", "170", "10", "80"), column_types=("Name", "age", "phone", "Name", "Name", "price", "Date_dont_use_time"),
                         data_active_index=7)

        self.right_click_commands = [["Επεξεργασία", self.edit],
                                     ["Φάκελος Θεραπευόμενου",
                                         self.open_patients_folder]
                                     ]
        self.selected_patient = None
        self.edit_patient_window = None
        self.SORT_ASCENDING = False
        self.sort_and_display_data(column=self.heading_names[6])

    def edit(self, row_id):
        self.set_selected_patient(row_id)

        # create popup window
        self.edit_patient_window = customtkinter.CTkToplevel(self)
        self.edit_patient_window.grab_set()
        self.edit_patient_window.focus_set()

        # place the window in the center of the screen
        screen_width = self.edit_patient_window.winfo_screenwidth()
        screen_height = self.edit_patient_window.winfo_screenheight()
        window_width = 1150
        window_height = 850
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        self.edit_patient_window.geometry("%dx%d+%d+%d" %
                                          (window_width, window_height, x_coord, y_coord))

        self.edit_patient_window.title("Επεξεργασία Θεραπευόμενου")
        edit_patient_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.edit_patient_window, fg_color=("transparent"))
        title_label = customtkinter.CTkLabel(
            edit_patient_scrollable_frame, text="Επεξεργασία στοιχείων θεραπευόμενου", font=self.manager.title_font)
        title_label.pack(expand=False, fill='none', padx=30, pady=30)
        self.edit_patient_window.protocol(
            "WM_DELETE_WINDOW", self.on_edit_patient_window_close)
        edit_patient_gui = EditPatientGUI(
            edit_patient_scrollable_frame, self.selected_patient, manager=self.manager, myfont=self.manager.main_font)
        edit_patient_gui.pack(expand=True, fill='both', padx=30, pady=30)
        edit_patient_scrollable_frame.pack(expand=True, fill='both')

    def on_edit_patient_window_close(self):
        self.manager.update_tables("patients")
        self.edit_patient_window.destroy()

    def open_patients_folder(self, row_id):
        """Opens the patients folder in the file explorer"""
        self.set_selected_patient(row_id)

        try:

            self.selected_patient.open_folder()

        except (FileNotFoundError, AttributeError) as err:

            MessageBox(
                "Error", err, "error")

    def set_selected_patient(self, row_id):

        patients_id = self.table.item(row_id)['values'][8]
        self.selected_patient = Patient(unique_id=patients_id)
        self.selected_patient.get_values_from_database_based_on_id()

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
        if self.manager is not None:
            if hasattr(self.manager, "update_patients_info_label"):
                self.manager.update_patients_info_label()


class UnconfirmedSessionsTable(CustomTable):

    def __init__(self, master, manager=None, heading_names=['Ημερομηνία', 'Ώρα', 'Περιγραφή', 'Ταυτοποιημένο Όνομα'],
                 column_widths=[80, 50, 400, 200], column_types=['Date', 'Time', 'Name', 'Name'], data_active_index=5):
        self.manager = manager
        super().__init__(master, manager=manager, heading_names=heading_names, column_widths=column_widths,
                         column_types=column_types, data_active_index=data_active_index)
        self.SORT_ASCENDING = False
        self.sort_and_display_data(column=self.heading_names[0])
        self.right_click_commands = [["Επιβεβαίωση", self.confirm],
                                     ["Αγνόησέ το", self.ignore]]

    def confirm(self, row_id):

        row = self.table.item(row_id)['values']
        this_patient = Patient(name=row[3])
        print(this_patient.name)
        if not this_patient.exists_in_database():
            MessageBox(
                "Σφάλμα", "Ο θεραπευόμενος δεν υπάρχει στη βάση δεδομένων.Καταχωρήστε πρώτα τον θεραπευόμενο.", "error")
            return

        top_level_window = customtkinter.CTkToplevel(self)
        top_level_window.title("Επιβεβαίωση Συνεδρίας")
        screen_width = top_level_window.winfo_screenwidth()
        screen_height = top_level_window.winfo_screenheight()
        window_width = 900
        window_height = 500
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        top_level_window.geometry("%dx%d+%d+%d" %
                                  (window_width, window_height, x_coord, y_coord))
        top_level_window.resizable(False, False)
        top_level_window.grab_set()
        top_level_window.focus_set()

        confirm_gui = NewSessionGUI(
            master=top_level_window, manager=self.manager, self_destroy=True, confirmation_mode=True)
        confirm_gui.title_label.configure(text="Επιβεβαίωση Συνεδρίας")
        confirm_gui.today_button.destroy()
        confirm_gui.yesterday_button.destroy()
        confirm_gui.submit_button.configure(text="Επιβεβαίωση")

        this_patient.get_values_from_database_based_on_name()

        this_session = Session(
            this_patient, date_time=Session.convert_human_datetime_to_iso(row[0]+" "+row[1]), calendar_event_id=row[4], date_time_format="ISO")
        prev_session = this_patient.get_last_session_from_database()
        if prev_session is not None:

            this_session.paid = prev_session[3]
            this_session.receipt = prev_session[7]
            this_session.receipt_amount = prev_session[8]

        confirm_gui.set_session_entry(this_session)
        top_level_window.protocol(
            "WM_DELETE_WINDOW", top_level_window.destroy)

    def ignore(self, row_id):
        row = self.table.item(row_id)['values']
        GeneralDatabase.add_to_ignored_events(row)
        self.manager.update_tables("unconfirmed_sessions")

    def process_data_from_calendar(self, calendar_events) -> list[list[str]]:
        CALENDAR_DATETIME = 0
        CALENDAR_NAME = 1
        CALENDAR_EVENT_ID = 2

        DATE = 0
        TIME = 1
        UNIDENTIFIED_NAME = 2
        ESTIMATED_NAME = 3
        GOOGLE_EVENT_ID = 4
        CONFIRMED = 5

        output = []

        if calendar_events == []:
            return
        for calendar_event in calendar_events:
            if GeneralDatabase.is_in_ignored_events(calendar_event[CALENDAR_EVENT_ID]):
                continue
            if GeneralDatabase.exists_in_database(calendar_event[CALENDAR_EVENT_ID]):
                continue
            datetime_string = calendar_event[CALENDAR_DATETIME]
            unidentified_name = calendar_event[CALENDAR_NAME]
            google_event_id = calendar_event[CALENDAR_EVENT_ID]
            date = self.extract_date_from_datetime_string(datetime_string)
            _time = self.extract_time_from_datetime_string(datetime_string)
            estimated_name = ""
            output.append([date, _time, unidentified_name,
                          estimated_name, google_event_id, "1"])

        # We check if we can figure out who the patient is.If we can't then
        # we append zero so the table knows that this session has some ambiguity
        # and the user needs to confirm it manually.Data active index must therefore be 4

        for row in output:
            if row[UNIDENTIFIED_NAME] in self.manager.patients_names_set:
                row[CONFIRMED] = "1"
                row[ESTIMATED_NAME] = row[UNIDENTIFIED_NAME]
                continue
            identification_result = self.manager.identify_patient(
                row[UNIDENTIFIED_NAME])

            if 3 > identification_result[1] >= 0:
                row[CONFIRMED] = "1"
                row[ESTIMATED_NAME] = identification_result[0]

            else:
                row[CONFIRMED] = "0"
                row[ESTIMATED_NAME] = ""

        return output

    def set_data(self, data, reset_scroll=True):

        if data is None:
            self.data = []
            self.update_data(reset_scroll=reset_scroll)
            return
        self.data = self.process_data_from_calendar(data)

        self.update_data(reset_scroll=reset_scroll)

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

        if self.manager is not None:
            if hasattr(self.manager, "update_unconfirmed_sessions_info_label"):
                self.manager.update_unconfirmed_sessions_info_label()

    def extract_date_from_datetime_string(self, datetime_string):
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%dT%H:%M:%S%z')
        date = datetime_object.strftime("%d/%m/%Y")
        return date

    def extract_time_from_datetime_string(self, datetime_string):
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%dT%H:%M:%S%z')
        time = datetime_object.strftime("%H:%M")
        return time

    @ staticmethod
    def generate_ISO_datetime_string(date, time):

        date_object = datetime.strptime(date, '%d/%m/%Y')
        time_object = datetime.strptime(time, '%H:%M:%S')
        datetime_object = datetime.combine(
            date_object, time_object.time())
        # add Athens Greece timezone info to datetime object and dont use timedelta
        # because it will not work with daylight saving time
        # use pytz instead

        datetime_object = pytz.timezone(
            'Europe/Athens').localize(datetime_object)

        datetime_string = datetime_object.isoformat()
        return datetime_string


class IgnoredEventsTable(UnconfirmedSessionsTable):
    def __init__(self, master, manager=None):
        self.manager = manager
        self.master = master

        super().__init__(master=self.master, manager=self.manager,
                         heading_names=['Ημερομηνία', 'Ώρα', 'Περιγραφή'],
                         column_widths=[50, 50, 400], column_types=['Date', 'Time', 'Name'], data_active_index=4)
        self.right_click_commands = [["Σταμάτα να το αγνοείς", self.remove_from_ignored_events],
                                     ["Συνέχισε να το αγνοείς", self.do_nothing]]
        self.table.unbind("<Double-Button-1>")

    def remove_from_ignored_events(self, row_id):
        GeneralDatabase.remove_from_ignored_events(
            self.table.item(row_id)['values'][3])
        ignored_events = GeneralDatabase.get_ignored_events()
        self.set_data(ignored_events)
        self.manager.update_tables("unconfirmed_sessions")
        if ignored_events == []:
            self.master.destroy()

    def do_nothing(self, row_id):
        pass

    def set_data(self, data, reset_scroll=True):
        self.data = []
        for row in data:
            _date = datetime.strptime(
                row[0], '%d/%m/%Y %H:%M').strftime("%d/%m/%Y")
            _time = datetime.strptime(
                row[0], '%d/%m/%Y %H:%M').strftime("%H:%M")
            _name = row[1]
            _event_id = row[2]
            self.data.append([_date, _time, _name, _event_id, "0"])
        self.update_data(reset_scroll=reset_scroll)


class SessionsTable(CustomTable):
    ''' Table for patients'''

    def __init__(self, master, manager=None):
        self.manager = manager
        super().__init__(master, manager,
                         heading_names=["Ημερομηνία", "Ώρα",
                                        "Όνομα", "Τιμή", "Πληρώθηκε"],
                         column_widths=("100", "50", "150", "50", "50"), column_types=("Date", "Time", "Name", "price", "paid"),
                         data_active_index=4)

        self.SORT_ASCENDING = False
        self.sort_and_display_data(
            column=self.heading_names[0])
        self.right_clicked_row = None
        self.double_clicked_row = None

    def edit(self):

        selected_patient = Patient(
            unique_id=(self.table.item(self.double_clicked_row)['values'][5]))
        selected_patient.get_values_from_database_based_on_id()
        selected_session = Session(selected_patient, unique_identifier=(
            self.table.item(self.double_clicked_row)['values'][7]))
        selected_session.get_values_from_database_based_on_id()

        edit_session_window = customtkinter.CTkToplevel(self.master)
        edit_session_window.title("Επεξεργασία Συνεδρίας")
        edit_session_window.geometry("800x800")
        edit_session_window.grab_set()
        edit_session_window.focus_set()

        # place the window in the center of the screen
        screen_width = edit_session_window.winfo_screenwidth()
        screen_height = edit_session_window.winfo_screenheight()
        window_width = 880
        window_height = 380
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        edit_session_window.geometry("%dx%d+%d+%d" %
                                     (window_width, window_height, x_coord, y_coord))
        edit_session_window.resizable(False, False)
        edit_session_gui = NewSessionGUI(
            master=edit_session_window, manager=self.manager)

        def update_session(event=None):
            new_session = edit_session_gui.get_session_entry()[0]

            boolean_success = SessionsDatabase.update_session(
                selected_session, new_session)
            if boolean_success:
                date = datetime.strptime(
                    new_session.date_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
                time = datetime.strptime(
                    new_session.date_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M:%S")
                MessageBox("Επιτυχής ενημέρωση συνεδρίας",
                           f"Η συνεδρία {new_session.name} με ημερομηνία {date} και ώρα {time} ενημερώθηκε επιτυχώς ", option="success")
                edit_session_window.destroy()
                self.manager.update_tables("sessions")
            else:
                MessageBox(
                    "Αποτυχία ενημέρωσης συνεδρίας", "error", option="error")
        edit_session_gui.today_button.destroy()
        edit_session_gui.yesterday_button.destroy()

        edit_session_gui.title_label.configure(text="Επεξεργασία Συνεδρίας")
        edit_session_gui.submit_button.configure(text="Ενημέρωση")
        edit_session_gui.submit_button.configure(
            command=update_session)
        # Return key is bound to the submit button(command=on_submit) in the base class
        # but now we want it to be bound to the update_session function
        edit_session_gui.submit_button.unbind("<Return>")
        edit_session_gui.submit_button.bind("<Return>", update_session)
        edit_session_gui.set_session_entry(selected_session)
        # Disable some of the entries so the user can't change the patient's name
        # or the date or the time
        edit_session_gui.date_entry.configure(state="disabled")
        edit_session_gui.time_entry.configure(state="disabled")
        edit_session_gui.name_entry.configure(state="disabled")
        edit_session_gui.pack(fill="both", expand=True)

    def delete(self):

        selected_patient = Patient(
            unique_id=(self.table.item(self.right_clicked_row)['values'][5]))
        selected_patient.get_values_from_database_based_on_id()
        selected_session = Session(selected_patient, unique_identifier=(
            self.table.item(self.right_clicked_row)['values'][7]))
        selected_session.get_values_from_database_based_on_id()

        delete_session_window = customtkinter.CTkToplevel(self)
        delete_session_window.title("Διαγραφή Συνεδρίας")
        screen_width = delete_session_window.winfo_screenwidth()
        screen_height = delete_session_window.winfo_screenheight()
        window_width = 450
        window_height = 200
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        delete_session_window.geometry("%dx%d+%d+%d" %
                                       (window_width, window_height, x_coord, y_coord))
        delete_session_window.resizable(False, False)
        delete_session_window.grab_set()
        delete_session_window.focus_set()
        user_input = tk.BooleanVar()
        user_input.set(False)

        def on_yes():
            user_input.set(True)
            delete_session_window.destroy()

        def on_no():
            user_input.set(False)
            delete_session_window.destroy()
        delete_session_window.protocol(
            "WM_DELETE_WINDOW", delete_session_window.destroy)
        yes_button = customtkinter.CTkButton(delete_session_window,
                                             text="Ναι", width=100, height=50, command=on_yes)
        no_button = customtkinter.CTkButton(delete_session_window,
                                            text="Όχι", width=100, height=50, command=on_no)

        label = customtkinter.CTkLabel(
            delete_session_window, text=f"Διαγραφή της συνεδρίας του θεραπευόμενου {selected_patient.name} ;", font=("Bahnschrift SemiLight Bold", 16), wraplength=280)
        label.pack(side="top", padx=10, pady=10)
        yes_button.pack(side="left", padx=30, pady=10)
        no_button.pack(side="right", padx=30, pady=10)
        delete_session_window.wait_window(delete_session_window)

        if user_input.get():
            SessionsDatabase.delete_session(selected_session.unique_identifier)
            self.manager.update_tables("sessions")

        else:
            return

    def set_paid(self, arg):

        selected_patient = Patient(
            unique_id=(self.table.item(self.right_clicked_row)['values'][5]))
        selected_patient.get_values_from_database_based_on_id()
        selected_session = Session(selected_patient, unique_identifier=(
            self.table.item(self.right_clicked_row)['values'][7]))
        selected_session.get_values_from_database_based_on_id()
        paid_dict = {"not_paid": 0,
                     "cash": 1,
                     "paypal": 2,
                     "credit_card": 3,
                     "bank": 4
                     }

        try:
            value = paid_dict[arg]

        except KeyError:
            print("Key Error in set_paid()")

        if selected_session.paid != value:

            selected_session.set_paid(paid_dict[arg])
            self.manager.update_tables("sessions")

        else:

            return

    def on_double_click(self, event):
        row = self.table.identify_row(event.y)
        self.double_clicked_row = row
        if row:
            self.edit()
        else:
            print("No row was clicked")
            return

    def fill_table(self, show_inactive=True):
        # time = datetime.now()

        self.table.delete(*self.table.get_children())
        self.displayed_data = []
        for row in self.data_to_display:
            status = 'active' if self.data_active_index is None else 'inactive' if row[
                self.data_active_index] == '0' else 'active'
            if not show_inactive and status == 'inactive':
                continue
            paid_text = ""
            if row[self.data_active_index] == '0':
                paid_text = "Όχι"
            elif row[self.data_active_index] == '1':
                paid_text = "Μετρητά"
            elif row[self.data_active_index] == '2':
                paid_text = "Paypal"
            elif row[self.data_active_index] == '3':
                paid_text = "Πιστωτική κάρτα"
            elif row[self.data_active_index] == '4':
                paid_text = "Τράπεζα"

            values = tuple(
                element if index != self.data_active_index else paid_text for index, element in enumerate(row))

            self.table.insert('', 'end', values=values, tags=status)
            self.displayed_data.append(row)
        if hasattr(self.manager, "sessions_table_for_view_sessions"):
            self.manager.update_stats()

    def on_right_click(self, event):

        row_id = self.table.identify('row', event.x, event.y)
        self.table.focus(row_id)

        if row_id:
            self.right_clicked_row = row_id
            if row_id != self.table.previous_selection:
                self.table.selection_set(row_id)
                self.table.previous_selection = row_id
            context_menu = tk.Menu(self, tearoff=0)
            paid_menu = tk.Menu(self, tearoff=0)

            context_menu.add_command(
                label="Επεξεργασία", command=lambda arg=event: self.on_double_click(arg), font=('Bahnschrift SemiLight', 12))
            context_menu.add_command(
                label="Δεν έχει πληρωθεί", command=lambda arg="not_paid": self.set_paid(arg), font=('Bahnschrift SemiLight', 12))

            context_menu.add_cascade(
                label="Έχει πληρωθεί", menu=paid_menu, font=('Bahnschrift SemiLight', 12))
            context_menu.add_separator()
            context_menu.add_command(
                label="Διαγραφή", command=self.delete, font=('Bahnschrift SemiLight', 12))
            paid_menu.add_command(
                label="Μετρητά", command=lambda arg="cash": self.set_paid(arg), font=('Bahnschrift SemiLight', 12))
            paid_menu.add_command(
                label="Paypal", command=lambda arg="paypal": self.set_paid(arg), font=('Bahnschrift SemiLight', 12))
            paid_menu.add_command(
                label="Πιστωτική κάρτα", command=lambda arg="credit_card": self.set_paid(arg), font=('Bahnschrift SemiLight', 12))
            paid_menu.add_command(
                label="Τράπεζα", command=lambda arg="bank": self.set_paid(arg), font=('Bahnschrift SemiLight', 12))

            # Display the context menu
            context_menu.tk_popup(event.x_root, event.y_root)
