"""This module contains the GUI for viewing a patient's details."""

# import copy
import tkinter as tk
from sqlite3 import Error, DatabaseError, OperationalError
from tkinter import filedialog
import customtkinter
from patient import Patient
from tdamourakis_ctkinter import MessageBox
from PIL import Image
from new_patient_gui import NewPatientGUI


class EditPatientGUI(NewPatientGUI):
    """This class creates a new window for viewing a patient's details."""

    def __init__(self, master,  patient: Patient, myfont=None, manager=None):
        self.patient = patient
        self.master = master
        self.manager = manager
        self.previous_text = ""
        self.widget_being_edited = None
        self.myfont = myfont

        self.edit_finished = True
        super().__init__(master, grid=False, myfont=self.myfont, manager=self.manager)
        self.main_frame.configure(bg_color="transparent")
        self.set_patient_entry(patient)
        self.status_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Κατάσταση:")
        self.status_combobox = customtkinter.CTkOptionMenu(self.main_frame, values=[
            "Ενεργή", "Ανενεργή"], font=(self.myfont),  width=190, text_color_disabled='black', text_color='black',  fg_color="thistle", dropdown_fg_color='thistle', dropdown_font=(self.myfont.cget("family"), 16), anchor="center")
        self.status_combobox.set("Ενεργή" if patient.active else "Ανενεργή")

        self.name_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=1), cursor="hand2")
        self.session_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=2), cursor="hand2")
        self.start_date_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=3), cursor="hand2")
        self.referenced_by_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=4), cursor="hand2")
        self.age_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=5), cursor="hand2")
        self.telephone_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=6), cursor="hand2")
        self.emergency_phone_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=7), cursor="hand2")
        self.address_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=8), cursor="hand2")
        self.profession_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=9), cursor="hand2")
        self.marital_status_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=10), cursor="hand2")
        self.children_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=11), cursor="hand2")
        self.medical_diagnosis_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=12), cursor="hand2")
        self.medical_prescription_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=13), cursor="hand2")
        self.request_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=14), cursor="hand2")
        self.price_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=15), cursor="hand2")
        self.status_edit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/pencil.png"),
                                                                                        dark_image=Image.open(
                "images/pencil.png")), command=lambda:  self.on_edit_button_press(button_id=17), cursor="hand2")
        # submit buttons
        self.name_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=1), cursor="hand2")
        self.session_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=2), cursor="hand2")
        self.start_date_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=3), cursor="hand2")
        self.referenced_by_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=4), cursor="hand2")
        self.age_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=5), cursor="hand2")
        self.telephone_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=6), cursor="hand2")
        self.emergency_phone_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=7), cursor="hand2")
        self.address_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=8), cursor="hand2")
        self.profession_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=9), cursor="hand2")
        self.marital_status_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=10), cursor="hand2")
        self.children_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=11), cursor="hand2")
        self.medical_diagnosis_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=12), cursor="hand2")
        self.medical_prescription_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=13), cursor="hand2")
        self.request_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=14), cursor="hand2")
        self.price_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=15), cursor="hand2")
        self.status_edit_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=lambda:  self.on_edit_submit_button_press(button_id=17), cursor="hand2")
        self.attach_file_submit_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/success.ico"),
                                                                                        dark_image=Image.open(
                "images/success.ico")), command=self.on_submit_files, cursor="hand2")

        self.attributes = [[self.name_label, self.name_entry, self.name_edit_button, self.name_edit_submit_button],
                           [self.session_label, self.session_type_combobox,
                           self.session_edit_button, self.session_edit_submit_button],
                           [self.start_date_label, self.start_date_entry,
                               self.start_date_edit_button, self.start_date_edit_submit_button],
                           [self.referenced_by_label, self.referenced_by_entry,
                           self.referenced_by_edit_button, self.referenced_by_edit_submit_button],
                           [self.age_label, self.age_entry,
                           self.age_edit_button, self.age_edit_submit_button],
                           [self.telephone_label, self.telephone_entry,
                           self.telephone_edit_button, self.telephone_edit_submit_button],
                           [self.emergency_phone_label, self.emergency_phone_entry,
                           self.emergency_phone_edit_button, self.emergency_phone_edit_submit_button],
                           [self.address_label, self.address_entry,
                           self.address_edit_button, self.address_edit_submit_button],
                           [self.profession_label, self.profession_entry,
                           self.profession_edit_button, self.profession_edit_submit_button],
                           [self.marital_status_label,
                           self.marital_status_combobox, self.marital_status_edit_button, self.marital_status_edit_submit_button],
                           [self.children_label, self.children_entry,
                           self.children_edit_button, self.children_edit_submit_button],
                           [self.medical_diagnosis_label,
                           self.medical_diagnosis_entry, self.medical_diagnosis_edit_button, self.medical_diagnosis_edit_submit_button],
                           [self.medical_prescription_label,
                           self.medical_prescription_entry, self.medical_prescription_edit_button, self.medical_prescription_edit_submit_button],
                           [self.request_label, self.request_entry,
                           self.request_edit_button, self.request_edit_submit_button],
                           [self.price_label, self.price_entry,
                           self.price_edit_button, self.price_edit_submit_button],
                           [self.attach_file_button, self.attach_file_entry,
                           self.attach_file_clear_button, self.attach_file_submit_button],
                           [self.status_label, self.status_combobox,
                               self.status_edit_button, self.status_edit_submit_button]


                           ]
        for index, attribute in enumerate(self.attributes):
            # pylint: disable=unused-variable
            if len(attribute) > 1:
                attribute[1].bind('<Return>', self.on_enter_press)
                if attribute[1] != self.attach_file_entry and (isinstance(attribute[1], customtkinter.CTkEntry) or isinstance(attribute[1], customtkinter.CTkOptionMenu) or isinstance(attribute[1], customtkinter.CTkTextbox)):
                    attribute[1].bind(
                        '<Double-Button-1>', lambda event, idx=index: self.on_edit_button_press(idx+1))

        self.grid_widgets()

        self.disable()
        self.color_entry_boxes(color='thistle')

    def color_entry_boxes(self, color):
        """Colors the entry boxes"""
        for attribute in self.attributes:
            for widget in attribute:
                if isinstance(widget, customtkinter.CTkEntry) or isinstance(widget, customtkinter.CTkTextbox):
                    widget.configure(fg_color=("thistle", "gray20"))

    def disable_to_display_message(self):
        """Disables all the widgets in the frame"""
        for attribute in self.attributes:
            for widget in attribute:
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.configure(state='disabled')
                elif isinstance(widget, customtkinter.CTkOptionMenu):
                    widget.configure(state='disabled')
                    widget.configure(cursor="arrow")
                elif isinstance(widget, customtkinter.CTkButton):
                    widget.configure(state='disabled')
                    widget.configure(cursor="arrow")

    def grid_widgets(self):
        """Packs all the widgets in the frame"""

        for i, attribute in enumerate(self.attributes):
            for j, element in enumerate(attribute):

                if element == self.attach_file_button:
                    element.grid(row=i, column=j, padx=30, pady=10)
                elif isinstance(element, customtkinter.CTkButton):

                    element.grid(row=i, column=j, padx=0,
                                 pady=0, sticky='w')
                    if j > 2:

                        element.grid_remove()

                else:
                    element.grid(row=i, column=j, padx=30,
                                 pady=5, sticky='nsew')

    def on_submit(self):
        """ Makes all necessary checks before submitting the form"""
        messages = ["Παρακαλώ εισάγετε το ονοματεπώνυμο του θεραπευόμενου.Επιτρέπονται μόνο γράμματα.",

                    "Παρακαλώ εισάγετε την ηλικία του θεραπευόμενου.Επιτρέπονται μόνο αριθμοί.",
                    "Παρακαλώ εισάγετε τον αριθμό τηλεφώνου του θεραπευόμενου.Επιτρέπονται μόνο αριθμοί και το '+'.\nΓια περισσότερα από ένα τηλέφωνα, χωρίστε τα με κενό.",
                    "Παρακαλώ εισάγετε το επάγγελμα του θεραπευόμενου.Επιτρέπονται μόνο γράμματα.",
                    "Για το πεδίο 'παιδιά' επιτρέπονται μόνο αριθμοί και ','",
                    "Παρακαλώ εισάγετε την τιμή της συνεδρίας του θεραπευόμενου.Επιτρέπονται μόνο αριθμοί και '€' '£' ή '$' (Το νόμισμα είναι προαιρετικό)"]
        edited_patient = self.get_patient_entry()
        edited_patient.active = 1 if self.status_combobox.get() == "Ενεργή" else 0

        fields = [edited_patient.name,
                  edited_patient.age,
                  edited_patient.telephone,
                  edited_patient.profession,
                  edited_patient.children,
                  edited_patient.price]
        entries = [self.name_entry,
                   self.age_entry,
                   self.telephone_entry,
                   self.profession_entry,
                   self.children_entry,
                   self.price_entry]
        functions = [edited_patient.has_valid_name,
                     edited_patient.has_valid_age,
                     edited_patient.has_valid_telephone,
                     edited_patient.has_valid_profession,
                     edited_patient.has_valid_children,
                     edited_patient.has_valid_price]
        for i in range(len(fields)):
            if not functions[i]():
                old_color = entries[i].cget("fg_color")
                entries[i].configure(fg_color="salmon")

                MessageBox("Σφάλμα", messages[i], "error")

                entries[i].configure(fg_color=old_color)

                return False

        # If the data is valid
        # then we update the patients object values
        # and database entry and add any new files submited

        self.patient.name = edited_patient.name
        self.patient.session_type = edited_patient.session_type
        self.patient.start_date = edited_patient.start_date
        self.patient.referenced_by = edited_patient.referenced_by
        self.patient.age = edited_patient.age
        self.patient.telephone = edited_patient.telephone
        self.patient.emergency_phone = edited_patient.emergency_phone
        self.patient.address = edited_patient.address
        self.patient.profession = edited_patient.profession
        self.patient.marital_status = edited_patient.marital_status
        self.patient.children = edited_patient.children
        self.patient.medical_diagnosis = edited_patient.medical_diagnosis
        self.patient.medical_prescription = edited_patient.medical_prescription
        self.patient.request = edited_patient.request
        self.patient.price = edited_patient.price
        self.patient.active = edited_patient.active

        try:
            self.patient.update_patient(self.patient.unique_id)
        except (Error, DatabaseError, OperationalError) as exp:

            MessageBox(
                "Σφάλμα", f"Παρουσιάστηκε σφάλμα κατά την εγγραφή στη βάση δεδομένων {exp}", "error")

            return False

        MessageBox(
            "Επιτυχής ενημέρωση βάσης δεδομένων!", "Επιτυχής τροποποίηση στοιχείων!", option="success")

        return True

    def on_edit_button_press(self, button_id):
        if not self.edit_finished:
            return
        self.widget_being_edited = self.attributes[button_id-1][1]
        self.edit_finished = False

        self.previous_text = self.get_widgets_text(
            self.attributes[button_id-1][1])
        self.attributes[button_id-1][1].configure(state="normal")
        if button_id not in (2, 10, 17):
            self.attributes[button_id -
                            1][1].configure(fg_color=("white", "gray10"))
        self.attributes[button_id-1][3].grid()

    def get_widgets_text(self, widget):
        """Returns the text of the widget"""
        if isinstance(widget, customtkinter.CTkEntry):
            return widget.get().strip()
        if isinstance(widget, customtkinter.CTkOptionMenu):
            return widget.get()
        if isinstance(widget, customtkinter.CTkTextbox):
            return widget.get("0.0", "end").strip()

    def set_widgets_text(self, widget, text):
        """Sets the text of the widget"""
        if isinstance(widget, customtkinter.CTkEntry):
            widget.delete(0, "end")
            widget.insert(0, text)

            return
        if isinstance(widget, customtkinter.CTkOptionMenu):
            widget.set(text)
            return
        if isinstance(widget, customtkinter.CTkTextbox):
            widget.delete("0.0", "end")
            widget.insert("0.0", text)

            return

    def on_edit_submit_button_press(self, button_id):
        """This function is called when the user presses the submit button"""
        # first we check if the user has changed the value of the entry
        if self.previous_text == self.get_widgets_text(self.attributes[button_id-1][1]):

            self.set_widgets_text(
                self.attributes[button_id-1][1], self.previous_text)
            if button_id not in (2, 10, 17):
                self.attributes[button_id -
                                1][1].configure(fg_color=("thistle", "gray20"))

            self.attributes[button_id-1][1].configure(state="disabled")
            self.attributes[button_id-1][3].grid_remove()
            self.edit_finished = True
            self.widget_being_edited = None
            self.previous_text = ""
            return

        if not self.on_submit():  # on_submit returns False if the data is invalid or there is an error
            self.set_widgets_text(
                self.attributes[button_id-1][1], self.previous_text)
            self.edit_finished = False
        else:

            self.attributes[button_id-1][3].grid_remove()
            self.attributes[button_id-1][1].configure(state="disabled")
            if button_id not in (2, 10, 17):
                self.attributes[button_id -
                                1][1].configure(fg_color=("thistle", "gray20"))
            self.edit_finished = True
            self.widget_being_edited = None
            self.previous_text = ""

            self.clear_files()

    def attach_file(self):
        """Opens a file dialog and appends the selected file to the files list"""

        if not self.edit_finished and self.widget_being_edited != self.attach_file_entry:
            return

        self.widget_being_edited = self.attach_file_entry
        modal_window = tk.Toplevel(self)
        modal_window.withdraw()  # Hide the modal window

        # Make the modal window modal, disabling the parent window
        modal_window.grab_set()

        self.previous_text = self.attributes[15][1].get()
        self.edit_finished = False
        self.attach_file_submit_button.grid()
        filenames = filedialog.askopenfilenames(
            initialdir="/", title="Select files", filetypes=(("All Files", "*.*"),), multiple=True, parent=modal_window)
        modal_window.grab_release()
        modal_window.destroy()
        if filenames:

            self.attach_file_clear_button.configure(state='normal')
            for filename in filenames:
                if filename not in self.files:
                    self.files.append(filename)

            self.attach_file_entry.configure(state='normal')
            self.attach_file_entry.delete(0, 'end')
            self.attach_file_entry.configure(font=("Verdana", 12))
            for i, file in enumerate(self.files):
                # print(file)
                if i == len(self.files) - 1:
                    self.attach_file_entry.insert('end', file.split("/")[-1])
                else:
                    self.attach_file_entry.insert(
                        'end', file.split("/")[-1] + ",")
            self.attach_file_entry.configure(state='disabled')

        # This is executed if the user presses cancel AND there are no selected files
        elif self.previous_text == "Δεν έχει επιλεγεί αρχείο":
            self.widget_being_edited = None
            self.edit_finished = True
            self.attach_file_submit_button.grid_remove()
        # This is executed if the user presses cancel AND there ARE selected files
        else:
            pass

    def on_enter_press(self, event):
        # pylint: disable=unused-argument
        # print("Hello from on_enter_press")
        focused_widget = str(self.master.focus_get()).rsplit(".", 1)[0]
        # print(
        #    f"focused_widget: {focused_widget} self.widget_being_edited: {self.widget_being_edited}")
        if focused_widget == str(self.widget_being_edited):
            # print(
            #    "Hello from on_enter_press if focused_widget == self.widget_being_edited:")
            for row, attribute in enumerate(self.attributes):
                for widget in attribute:
                    if str(widget) == focused_widget:
                        self.on_edit_submit_button_press(row+1)
                        break

    def on_submit_files(self):
        self.patient.attached_files = self.files
        if self.patient.attached_files != []:
            try:
                # print(self.patient.attached_files)

                self.patient.copy_files_to_folder(
                    self.patient.attached_files)
            except (FileExistsError, PermissionError, FileNotFoundError, OSError) as exp:

                MessageBox(
                    "Σφάλμα", f"Παρουσιάστηκε σφάλμα κατά την αντιγραφή:\n  {exp}", option="error")
                self.clear_files()

                return False
            filenames = ""

            if len(self.patient.attached_files) == 1:

                message = "του αρχείου"
            else:

                message = "των αρχείων:"
            for i, file in enumerate(self.patient.attached_files):
                # print(file)
                if i == len(self.patient.attached_files) - 1:
                    filenames = filenames+file.split("/")[-1]
                else:
                    filenames = filenames+file.split("/")[-1] + ","

            for char in filenames:

                if char == ',':
                    filenames = filenames.replace(",", "\n-")
            # print(filenames)
            filenames = '\n-'+filenames+'\n'
            MessageBox("Επιτυχής αντιγραφή!",
                       f"Εγινε αντιγραφή {message} {filenames} στον φάκελο του θεραπευόμενου!", option="success")

            self.clear_files()
            return True

    def clear_files(self):
        """Clears the files list and the entry widget"""
        self.files = []
        self.attach_file_entry.configure(state='normal')
        self.attach_file_entry.delete(0, 'end')
        self.attach_file_entry.insert(0, "Δεν έχει επιλεγεί αρχείο")
        self.attach_file_entry.configure(font=self.myfont)
        self.attach_file_entry.configure(state='disabled')
        self.attach_file_clear_button.configure(state='disabled')
        self.patient.attached_files = []
        self.attach_file_submit_button.grid_remove()
        self.edit_finished = True
        self.widget_being_edited = None
        self.previous_text = ""


if __name__ == "__main__":
    app = customtkinter.CTk()
    app.title("Επεξεργασία Θεραπευόμενου")
    patient_to_edit = Patient()
    edit_patient_gui = EditPatientGUI(app, patient_to_edit)
    edit_patient_gui.pack(fill="both", expand=True)
    app.mainloop()
