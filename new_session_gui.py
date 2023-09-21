""" This module contains the NewSessionGUI class which is the GUI for the new session window.
    

    """
# pylint: disable=unused-argument

from datetime import datetime, timedelta
from sqlite3 import Error, OperationalError, DatabaseError
from tkinter import ttk

from tdamourakis_ctkinter import MessageBox
import tkinter as tk


from unidecode import unidecode
from patients_management_database import PatientsDatabase

import customtkinter


from patient import Patient
from session import Session


class NewSessionGUI(customtkinter.CTkFrame):
    """ This class creates a new frame for adding a new lesson."""

    def __init__(self, master, manager, myfont=None, grid=None, self_destroy: bool = False, confirmation_mode: bool = False):
        self.self_destroy = self_destroy
        self.confirmation_mode = confirmation_mode
        self.set_session: Session = None
        super().__init__(master, corner_radius=20)
        self.master = master
        self.manager = manager

        self.configure(fg_color='transparent')
        self.color_index = 0

        if myfont is None:
            self.myfont = customtkinter.CTkFont(
                family='Bahnschrift SemiLight', size=20)
        else:
            self.myfont = myfont

        self.my_small_font = customtkinter.CTkFont(
            family='Bahnschrift SemiLight', size=18)

        self.button_style = ttk.Style()
        self.button_style.configure("button_style.TButton", font=self.myfont)

        self.patients: list[Patient] = PatientsDatabase.get_patients_as_objects(
            inactive=True)

        self.name_text_variable = tk.StringVar()
        self.date_text_variable = tk.StringVar()
        self.time_text_variable = tk.StringVar()
        self.price_text_variable = tk.StringVar()
        self.boolean_index = True
        self.dropdown_listbox = None

        self.name_text_variable.trace('w', self.on_name_entry_change)
        self.time_text_variable.trace('w', self.on_time_entry_change)

        self.title_label = customtkinter.CTkLabel(
            self, text="ΝΕΑ ΣΥΝΕΔΡΙΑ", font=customtkinter.CTkFont(
                family='Bahnschrift SemiLight', size=36))
        self.name_label = customtkinter.CTkLabel(
            self, text="Ονοματεπώνυμο:", font=self.myfont)
        self.name_entry = customtkinter.CTkEntry(
            self, textvariable=self.name_text_variable, font=self.myfont, height=25, width=350, justify="center")
        self.date_label = customtkinter.CTkLabel(
            self, text="Ημερομηνία Συνεδρίας:", font=self.myfont)
        self.date_entry = customtkinter.CTkEntry(
            self, textvariable=self.date_text_variable, font=self.myfont, height=25, width=350, justify="center")
        self.today_button = ttk.Button(
            self, text="Σήμερα",  width=10, style="button_style.TButton", command=self.on_today_button_pressed)
        self.yesterday_button = ttk.Button(
            self, text="Χθες",  width=10, style="button_style.TButton", command=self.on_yesterday_button_pressed)
        self.time_label = customtkinter.CTkLabel(
            self, font=self.myfont, text="Ώρα Συνεδρίας:")
        self.time_entry = customtkinter.CTkEntry(
            self, textvariable=self.time_text_variable, font=self.myfont, height=25, width=350, justify="center")
        self.paid_label = customtkinter.CTkLabel(
            self, font=self.myfont, text="Πληρωμένο:")
        self.paid_var = tk.StringVar()
        self.price_text_variable.trace('w', self.on_price_entry_change)

        self.option_add("*TCombobox*Listbox*Font", self.my_small_font)
        self.paid_var.trace_add("write", self.checkbox_update)
        self.receipt_checkbox = customtkinter.CTkCheckBox(self, text="Απόδειξη", command=self.checkbox_event, font=self.myfont,
                                                          onvalue="on", offvalue="off")
        self.receipt_entry = customtkinter.CTkEntry(
            self, font=self.myfont, height=25, width=50, justify="left")
        self.paid_entry = ttk.Combobox(self, textvariable=self.paid_var, font=self.myfont, values=[
            "Όχι", "Μετρητά", "Paypal", "Πιστωτική κάρτα", "Τράπεζα"], state="readonly", justify="center")
        self.paid_entry.set("Όχι")
        self.paid_entry.config(font=self.myfont)

        self.price_label = customtkinter.CTkLabel(
            self, text="Τιμή Συνεδρίας:", font=self.myfont)
        self.price_entry = customtkinter.CTkEntry(
            self, textvariable=self.price_text_variable, font=self.myfont, height=25, width=350, justify="center")

        self.time_entry.bind('<Tab>', self.focus_paid_entry)

        self.submit_button = ttk.Button(
            self, text="Καταχώρηση", width=25,  style="button_style.TButton", command=self.on_submit)
        self.pack(fill="none", expand=True)

        self.entries = [self.name_entry,
                        self.date_entry,
                        self.time_entry,
                        self.price_entry]

        self.attributes = [[self.title_label],
                           [self.name_label, self.name_entry],
                           [self.date_label, self.date_entry,
                           self.today_button, self.yesterday_button],
                           [self.time_label, self.time_entry],
                           [self.paid_label, self.paid_entry,
                               self.receipt_checkbox, self.receipt_entry],
                           [self.price_label, self.price_entry],
                           [self.submit_button]
                           ]
        if grid is not False:
            self.grid_widgets()

        self.name_entry.bind('<Down>', self.on_key_down)
        self.name_entry.bind('<Up>', self.on_key_up)
        self.name_entry.bind('<Return>', self.on_patient_select)
        self.name_entry.bind('<Escape>', self.on_escape)

        self.today_button.bind('<Return>', self.on_today_button_pressed)
        self.yesterday_button.bind(
            '<Return>', self.on_yesterday_button_pressed)
        self.submit_button.bind('<Return>', self.on_submit)

    def on_price_entry_change(self, *args):

        self.receipt_entry.delete(0, 'end')
        self.receipt_entry.insert('end', self.price_entry.get())

    def checkbox_event(self):

        if self.receipt_checkbox.get() == "on":
            self.receipt_entry.grid(row=4, column=3, sticky="w")
        else:
            self.receipt_entry.grid_forget()

    def checkbox_update(self, *args):

        if self.paid_var.get() == "Όχι":
            self.receipt_checkbox.deselect()
            self.receipt_checkbox.configure(state="disabled")
            self.receipt_entry.grid_forget()

        elif self.paid_var.get() == "Μετρητά":
            self.receipt_checkbox.configure(state="normal")
            self.receipt_checkbox.deselect()
            self.receipt_entry.grid_forget()
        elif self.paid_var.get() == "Paypal":
            self.receipt_checkbox.configure(state="normal")
            self.receipt_checkbox.deselect()
            self.receipt_entry.grid_forget()
        elif self.paid_var.get() == "Πιστωτική κάρτα":
            self.receipt_checkbox.configure(state="enabled")
            self.receipt_checkbox.select()
            self.receipt_entry.delete(0, 'end')
            self.receipt_entry.insert('end', self.price_entry.get())
            self.receipt_entry.grid(row=4, column=3, sticky="w")
        elif self.paid_var.get() == "Τράπεζα":
            self.receipt_checkbox.configure(state="enabled")
            self.receipt_checkbox.select()
            self.receipt_entry.delete(0, 'end')
            self.receipt_entry.insert('end', self.price_entry.get())
            self.receipt_entry.grid(row=4, column=3, sticky="w")

    def focus_paid_entry(self, event=None):
        self.paid_entry.focus_set()
        self.after(100, lambda: self.paid_entry.event_generate('<Button-1>'))
        return "break"

    def on_today_button_pressed(self, event=None):
        self.date_text_variable.set(datetime.today().strftime("%d/%m/%Y"))

    def on_yesterday_button_pressed(self, event=None):
        self.date_text_variable.set(
            (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y"))

    def on_name_entry_change(self, *args):

        # Destroy the existing dropdown, if it exists
        if hasattr(self, 'dropdown_listbox') and self.dropdown_listbox is not None:
            self.dropdown_listbox.destroy()

        # Get the entered text
        typed_name = self.name_entry.get()

        if typed_name:
            # Find matching patient names
            matching_patients = [
                patient for patient in self.patients if unidecode(typed_name.lower()) in unidecode(patient.name.lower())]

            # If matches are found, create the dropdown list
            if matching_patients:
                max_name_length = max(len(patient.name)
                                      for patient in matching_patients)
                self.dropdown_listbox = tk.Listbox(self, font=self.myfont, height=len(matching_patients),
                                                   width=max_name_length + 2, bg='floral white')

                # Populate the listbox with matching patient names
                for patient in matching_patients:
                    self.dropdown_listbox.insert('end', patient.name)

                # Place the listbox below the name_entry
                self.dropdown_listbox.place(x=self.name_entry.winfo_x(
                ), y=self.name_entry.winfo_y() + self.name_entry.winfo_height())

                # Bind the listbox selection event to set the selected patient name in the name_entry
                # self.name_entry.bind(
                # "<<ListboxSelect>>", self.on_patient_select)
                # When the user presse the down arrow, the listbox will be focused

            else:
                self.dropdown_listbox = None
        else:
            self.dropdown_listbox = None

    def on_key_down(self, event=None):
        if self.dropdown_listbox is not None:
            current_selection = self.dropdown_listbox.curselection()
            if current_selection:
                current_index = current_selection[0]
                next_index = min(current_index + 1,
                                 self.dropdown_listbox.size() - 1)
                self.dropdown_listbox.selection_clear(current_index)
                self.dropdown_listbox.selection_set(next_index)
                self.dropdown_listbox.see(next_index)
            else:
                self.dropdown_listbox.selection_set(0)

    def on_key_up(self, event):

        if self.dropdown_listbox is not None:
            current_selection = self.dropdown_listbox.curselection()

            if current_selection:
                current_index = current_selection[0]
                prev_index = max(current_index - 1, 0)
                self.dropdown_listbox.selection_clear(current_index)
                self.dropdown_listbox.selection_set(prev_index)
                self.dropdown_listbox.see(prev_index)

    def on_escape(self, event):
        self.dropdown_listbox.destroy()
        self.dropdown_listbox = None

    def on_time_entry_change(self, *args):

        number_of_digits = len(self.time_text_variable.get().replace(":", ""))
        # now if the user types 2 digits, add a colon and move the cursor after the colon
        if number_of_digits < 2:
            self.boolean_index = True
        if number_of_digits == 2 and ":" not in self.time_text_variable.get() and self.boolean_index:
            self.time_text_variable.set(
                self.time_text_variable.get() + ":")
            text = self.time_text_variable.get()
            self.time_entry.delete(0, 'end')
            self.time_entry.insert('end', text)
            self.boolean_index = False
        if number_of_digits == 3 and ":" not in self.time_text_variable.get():
            self.time_text_variable.set(
                self.time_text_variable.get()[:2] + ":" + self.time_text_variable.get()[2:])
            text = self.time_text_variable.get()
            self.time_entry.delete(0, 'end')
            self.time_entry.insert('end', text)

    def clear_entries(self):

        for entry in self.entries:
            entry.delete(0, 'end')

    def on_patient_select(self, event):
        # Get the selected patient's name from the listbox
        selected_name = self.dropdown_listbox.get(
            self.dropdown_listbox.curselection())

        # Set the name_entry text to the selected patient's name
        self.name_entry.delete(0, 'end')
        self.name_entry.insert('end', selected_name)

        # Destroy the dropdown list
        self.dropdown_listbox.destroy()
        self.dropdown_listbox = None

        selected_patient: Patient = None
        # Now set the price entry to the patient's price
        for patient in self.patients:
            if patient.name == selected_name:
                selected_patient = patient
                self.price_entry.delete(0, 'end')
                self.price_entry.insert('end', patient.price)
                break

        # Now look at the database and see what time does the patient have sessions
        # set the time entry to the time the patient had a session the last time
        previous_session = selected_patient.get_last_session_from_database()
        if len(previous_session) > 0:
            self.time_entry.delete(0, 'end')

            last_session_date_time = datetime.strptime(
                previous_session[1], "%Y-%m-%dT%H:%M:%S%z")
            last_session_time = last_session_date_time.time()
            self.time_entry.insert(
                'end', last_session_time.strftime("%H:%M"))  # Dont need seconds here

    def paid_entry_key_up(self, event=None):
        current_value = self.paid_var.get()
        if current_value == "Όχι":
            self.paid_var.set("Ναι")
        return "break"

    def paid_entry_key_down(self, event=None):
        current_value = self.paid_var.get()
        if current_value == "Ναι":
            self.paid_var.set("Όχι")
        return "break"

    def paid_entry_key_enter(self, event=None):
        self.paid_entry.event_generate("<<ComboboxSelected>>")
        return "break"

    def on_submit(self, event=None):
        """ Makes all necessary checks before submitting the form"""
        messages = ["Παρακαλώ εισάγετε το ονοματεπώνυμο του θεραπευόμενου.Επιτρέπονται μόνο γράμματα.",
                    "Παρακαλώ εισάγετε την ημερομηνία της συνεδρίας στη μορφή 'ΗΗ/ΜΜ/ΕΕΕΕ' και την ώρα της συνεδρίας στη μορφή 'ΩΩ:ΛΛ.",
                    "Παρακαλώ εισάγετε την τιμή της συνεδρίας.Επιτρέπονται μόνο αριθμοί και '€' '£' ή '$' (Το νόμισμα είναι προαιρετικό)"]
        try:

            session_entry = self.get_session_entry()
            session_obj = session_entry[0]
            patient_obj = session_entry[1]
        except (AttributeError, TypeError, ValueError) as exp:
            MessageBox(
                "Σφάλμα", "Παρακαλώ ελέγξτε τα δεδομένα που εισάγατε."+str(exp), "error")
            return

        functions = [session_obj.has_valid_name,
                     session_obj.has_valid_date_time,
                     session_obj.has_valid_price]

        validation = True
        old_color = ""

        for i, validation_check in zip([0, (1, 2), 2], functions):

            if not validation_check():
                if type(i) == tuple:
                    for j in i:

                        old_color = self.entries[j].cget("fg_color")
                        self.entries[j].configure(fg_color="salmon")
                        message_index = 1
                        entry_index = 1
                else:
                    if i == 2:
                        old_color = self.entries[i+1].cget("fg_color")
                        self.entries[i+1].configure(fg_color="salmon")
                        message_index = i
                        entry_index = 3
                    else:
                        old_color = self.entries[i].cget("fg_color")
                        self.entries[i].configure(fg_color="salmon")
                        message_index = i
                        entry_index = i

                validation = False
                break
        if not validation:
            MessageBox("Σφάλμα", messages[message_index], "error")
            for entry in self.entries:
                entry.configure(fg_color=old_color)
            self.entries[entry_index].focus()
            return
        elif not patient_obj.exists_in_database():
            MessageBox(
                "Σφάλμα", "Ο θεραπευόμενος δεν υπάρχει στη βάση δεδομένων.", "error")
            return

        _date = datetime.strptime(
            session_obj.date_time, "%Y-%m-%dT%H:%M:%S%z").date().strftime("%d/%m/%Y")
        _time = datetime.strptime(
            session_obj.date_time, "%Y-%m-%dT%H:%M:%S%z").time().strftime("%H:%M:%S")
        if session_obj.exists_in_database():

            MessageBox(
                "Σφάλμα", f"Η συνεδρία '{session_obj.name}' με ημ/νία {_date} και ώρα {_time} υπάρχει ήδη στη βάση δεδομένων.", "error")

        else:

            # If the data is valid and there is no duplicate entry in the database,
            # then we write to the database

            try:
                session_obj.write_yourself_to_database()
            except (Error, DatabaseError, OperationalError) as exp:

                MessageBox(
                    "Σφάλμα", f"Παρουσιάστηκε σφάλμα κατά την εγγραφή στη βάση δεδομένων {exp}", "error")

                return

            MessageBox(
                "Επιτυχία", f"Η συνεδρία '{session_obj.name}' με ημ/νία {_date} και ώρα {_time},καταχωρήθηκε επιτυχώς.", "success")

            self.clear_entries()

            if self.confirmation_mode:
                if self.self_destroy:
                    self.master.destroy()
                self.manager.update_tables("sessions")
                self.manager.update_tables("unconfirmed_sessions")
            else:
                self.manager.update_tables("sessions")

            if self.self_destroy:
                self.destroy()

    def grid_widgets(self):
        """Packs all the widgets in the frame"""

        for i, attribute in enumerate(self.attributes):
            for j, element in enumerate(attribute):
                if element == self.title_label:
                    element.grid(row=i, column=1,
                                 padx=8, pady=25, sticky='nsew')
                elif element == self.submit_button:
                    self.submit_button.grid(
                        row=i, column=1, padx=8, pady=5, sticky='nsew')
                elif element == self.today_button or element == self.yesterday_button:
                    element.grid(row=i, column=j, padx=2,
                                 pady=5, sticky='w')
                else:
                    element.grid(row=i, column=j, padx=8,
                                 pady=5, sticky='nsew')
        self.receipt_entry.grid_forget()

    def on_close(self):
        """Destroys the window and sets the master state to normal"""
        self.master.state('normal')
        self.grab_release()

        self.destroy()

    def set_session_entry(self, session_instance: Session):
        """Sets the lesson entry form to the values of the session object passed in"""
        self.set_session = session_instance
        self.clear_entries()
        self.name_entry.insert('end', session_instance.name)
        self.dropdown_listbox.destroy()
        self.dropdown_listbox = None

        self.date_entry.insert('end', datetime.strptime(session_instance.date_time, "%Y-%m-%dT%H:%M:%S%z").date().strftime(
            "%d/%m/%Y"))

        self.time_entry.insert('end', datetime.strptime(session_instance.date_time, "%Y-%m-%dT%H:%M:%S%z").time().strftime(
            "%H:%M"))

        payment = session_instance.paid

        if payment == 0:
            self.paid_entry.set("Όχι")
        elif payment == 1:
            self.paid_entry.set("Μετρητά")
        elif payment == 2:
            self.paid_entry.set("Paypal")
        elif payment == 3:
            self.paid_entry.set("Πιστωτική κάρτα")
        elif payment == 4:
            self.paid_entry.set("Τράπεζα")

        else:
            raise ValueError(f"Invalid payment value: {payment}")
        self.price_entry.delete(0, 'end')
        self.price_entry.insert('end', session_instance.price)

        if session_instance.receipt == 1:
            self.receipt_checkbox.select()
            self.receipt_entry.grid(row=4, column=3, sticky="w")

        self.receipt_entry.delete(0, 'end')
        self.receipt_entry.insert('end', session_instance.receipt_amount)
        if self.confirmation_mode:
            self.name_entry.configure(state="disabled")
            self.date_entry.configure(state="disabled")
            self.time_entry.configure(state="disabled")

    def get_session_entry(self):
        """Gets the entered values from the session entry form, removing any trailing whitespace"""
        if self.confirmation_mode == False:

            date_string = self.date_entry.get().strip()
            time_string = self.time_entry.get().strip()
            # if the user has entered an invalid date or time, converting it to iso will
            # raise an exception, so we catch it and set the date_time_obj to None
            # The error will be caught and handled in the on_submit method after calling the has_valid_date_time method

            date_time_obj = Session.convert_human_datetime_to_iso(
                date_string + " " + time_string)

            patient_obj = Patient(name=self.name_entry.get().strip())
            patient_obj.get_values_from_database_based_on_name()

            new_session = Session(patient_obj, date_time_obj,
                                  price=self.price_entry.get().strip())
        else:
            new_session = self.set_session
            new_session.price = self.price_entry.get().strip()
            patient_obj = new_session.patient_instance

        new_session.receipt = 1 if self.receipt_checkbox.get() == "on" else 0
        new_session.receipt_amount = self.receipt_entry.get(
        ).strip() if new_session.receipt == 1 else 0
        payment = self.paid_entry.get()

        if payment == "Μετρητά":
            new_session.paid = 1
        elif payment == "Paypal":
            new_session.paid = 2
        elif payment == "Πιστωτική κάρτα":
            new_session.paid = 3
        elif payment == "Τράπεζα":
            new_session.paid = 4
        elif payment == "Όχι":
            new_session.paid = 0

        return (new_session, patient_obj)


if __name__ == '__main__':
    root = customtkinter.CTk()
    print(PatientsDatabase.get_patients())

    root.mainloop()
