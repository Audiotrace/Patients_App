""" This module contains the NewPatientGUI class which is the GUI for the new patient window.
    It is a toplevel window that is opened when the user clicks the "Νέος Θεραπευόμενος" button in the main window.
    It contains all the widgets that are needed to create a new patient.

    """
# import time
# from random_patient import RandomPatient
from sqlite3 import Error, OperationalError, DatabaseError

from tdamourakis_ctkinter import MessageBox, Image
import tkinter as tk


from tkinter import filedialog
import customtkinter


from patient import Patient
# from random_patient import RandomPatient


class NewPatientGUI(customtkinter.CTkFrame):
    """
    This class is the GUI for the new patient window.
    It is a toplevel window that is opened when the user
    clicks the "Νέος Θεραπευόμενος" button in the main window.
    It contains all the widgets that are needed to create a new patient.
    """

    def __init__(self, master, manager, myfont=None, grid=None):
        if myfont is None:
            self.myfont = customtkinter.CTkFont(
                family='Bahnschrift SemiLight', size=24)

        else:
            self.myfont = myfont

        self.master = master
        self.manager = manager
        super().__init__(master)

        self.color_index = 0

        self.main_frame = customtkinter.CTkFrame(
            master=self, fg_color='transparent', width=1000, height=768)

        self.submit_button = customtkinter.CTkButton(
            self.main_frame, text="Καταχώρηση", font=(self.myfont), width=250, height=80, command=self.on_submit)
        self.attach_file_button = customtkinter.CTkButton(
            self.main_frame, text="Προσθήκη αρχείου:", font=(self.myfont), width=220, height=60, command=self.attach_file)
        self.attach_file_clear_button = customtkinter.CTkButton(
            self.main_frame, text="", width=25, height=25, image=customtkinter.CTkImage(light_image=Image.open("images/trash.ico"),
                                                                                        dark_image=Image.open(
                "images/trash.ico"),
                size=(25, 25)), command=self.clear_files)
        self.attach_file_clear_button.configure(state="disabled")
        self.attach_file_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, width=500, height=25, justify="center")
        self.attach_file_entry.insert(0, "Δεν έχει επιλεγεί αρχείο")
        self.attach_file_entry.configure(state="disabled")
        self.title_label = customtkinter.CTkLabel(
            self.main_frame, text="    Καταχώρηση Νέου Θεραπευόμενου", font=(self.myfont.cget("family"), 30))
        self.name_label = customtkinter.CTkLabel(
            self.main_frame, text="Ονοματεπώνυμο:", font=self.myfont)
        self.name_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.session_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Τρόπος διεξαγωγής συνεδρίας:")
        self.session_type_combobox = customtkinter.CTkOptionMenu(self.main_frame,
                                                                 values=["Διαδικτυακά",
                                                                         "Δια Ζώσης", "Τηλεφωνικά"], fg_color="thistle", text_color_disabled='black', text_color='black', dropdown_fg_color='thistle', font=(self.myfont), width=190,  dropdown_font=(self.myfont.cget("family"), 16), anchor="center")

        self.start_date_label = customtkinter.CTkLabel(
            self.main_frame, text="Ημερομηνία έναρξης:", font=self.myfont)
        self.start_date_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.referenced_by_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Προέλευση περιστατικού:")
        self.referenced_by_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.age_label = customtkinter.CTkLabel(
            self.main_frame, text="Ηλικία", font=self.myfont)
        self.age_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.telephone_label = customtkinter.CTkLabel(
            self.main_frame, text="Τηλέφωνο:", font=self.myfont)
        self.telephone_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.emergency_phone_label = customtkinter.CTkLabel(self.main_frame,
                                                            text="Τηλέφωνο έκτακτης ανάγκης:", font=self.myfont)
        self.emergency_phone_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.address_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Διεύθυνση κατοικίας")
        self.address_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.profession_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Επάγγελμα")
        self.profession_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.marital_status_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Οικογενειακή κατάσταση:")
        self.marital_status_combobox = customtkinter.CTkOptionMenu(self.main_frame, values=[
            "Άγαμος/η", "Σε μόνιμη σχέση", "Έγγαμος/η", "Διαζευγμένος/η", "Χήρος/α"], font=(self.myfont), text_color_disabled='black', text_color='black', dropdown_fg_color='thistle', fg_color="thistle", width=190,  dropdown_font=(self.myfont.cget("family"), 16), anchor="center")

        self.children_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Ηλικίες παιδιών")
        self.children_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.medical_diagnosis_label = customtkinter.CTkLabel(
            self.main_frame, text="Διαγνωσμένη ιατρική πάθηση:", font=self.myfont)
        self.medical_diagnosis_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.medical_prescription_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Φαρμακευτική Αγωγή")
        self.medical_prescription_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.request_label = customtkinter.CTkLabel(
            self.main_frame, font=self.myfont, text="Αίτημα:")
        self.request_entry = customtkinter.CTkTextbox(
            self.main_frame, font=self.myfont, height=75, width=500, border_width=2, fg_color=('#F9F9FA', '#343638'), wrap="word")
        self.price_label = customtkinter.CTkLabel(
            self.main_frame, text="Τιμή συνεδρίας:", font=self.myfont)
        self.price_entry = customtkinter.CTkEntry(
            self.main_frame, font=self.myfont, height=25, width=500, justify="center")
        self.files = []
        self.main_frame.pack(fill="none", expand=True)
        self.attributes = [[self.title_label],
                           [self.name_label, self.name_entry],
                           [self.session_label, self.session_type_combobox],
                           [self.start_date_label, self.start_date_entry],
                           [self.referenced_by_label, self.referenced_by_entry],
                           [self.age_label, self.age_entry],
                           [self.telephone_label, self.telephone_entry],
                           [self.emergency_phone_label, self.emergency_phone_entry],
                           [self.address_label, self.address_entry],
                           [self.profession_label, self.profession_entry],
                           [self.marital_status_label,
                            self.marital_status_combobox],
                           [self.children_label, self.children_entry],
                           [self.medical_diagnosis_label,
                            self.medical_diagnosis_entry],
                           [self.medical_prescription_label,
                            self.medical_prescription_entry],
                           [self.request_label, self.request_entry],
                           [self.price_label, self.price_entry],
                           [self.attach_file_button, self.attach_file_entry,
                            self.attach_file_clear_button],
                           [self.submit_button]
                           ]
        if grid is not False:
            self.grid_widgets()

    def clear_entries(self):
        for attribute in self.attributes:
            for widget in attribute:
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.delete(0, 'end')
        self.clear_files()

    def disable(self):
        """Disables all the widgets in the frame"""
        for attribute in self.attributes:
            for widget in attribute:
                if isinstance(widget, customtkinter.CTkEntry) or isinstance(widget, customtkinter.CTkTextbox):
                    widget.configure(state='disabled')
                elif isinstance(widget, customtkinter.CTkOptionMenu):
                    widget.configure(state='disabled')
                    widget.configure(cursor="arrow")

    def enable(self):
        """Enables all the widgets in the frame"""

        # You cant just enable the clear button, you have to check if the entry widget has a value
        # If it has the default value,it means it is supposed to be disabled.
        # The attach_file_entry should be always disabled unless we want to write something in it
        for attribute in self.attributes:
            for widget in attribute:
                if widget != self.attach_file_clear_button and widget != self.attach_file_entry:
                    widget.configure(state='normal')
                elif self.attach_file_entry.get() != "Δεν έχει επιλεγεί αρχείο":
                    self.attach_file_clear_button.configure(state='normal')

    def clear_files(self):
        """Clears the files list and the entry widget"""
        self.files = []
        self.attach_file_entry.configure(state='normal')
        self.attach_file_entry.delete(0, 'end')
        self.attach_file_entry.insert(0, "Δεν έχει επιλεγεί αρχείο")
        self.attach_file_entry.configure(font=self.myfont)
        self.attach_file_entry.configure(state='disabled')
        self.attach_file_clear_button.configure(state='disabled')
        if hasattr(self, "patient"):
            self.patient.attached_files = []

    def on_submit(self):
        """ Makes all necessary checks before submitting the form"""
        messages = ["Παρακαλώ εισάγετε το ονοματεπώνυμό μου! (Επιτρέπονται μόνο γράμματα)",
                    "Παρακαλώ εισάγετε την ηλικία μου!Επιτρέπονται μόνο αριθμοί.",
                    "Παρακαλώ εισάγετε τον αριθμό τηλεφώνου μου!Επιτρέπονται μόνο αριθμοί και το '+'.\nΓια περισσότερα από ένα τηλέφωνα, χωρίστε τα με κενό.",
                    "Παρακαλώ εισάγετε το επάγγελμά μου!Επιτρέπονται μόνο γράμματα.",
                    "Για το πεδίο 'παιδιά' επιτρέπονται μόνο αριθμοί και ','",
                    "Παρακαλώ εισάγετε την τιμή της συνεδρίας μου! Επιτρέπονται μόνο αριθμοί και '€' '£' ή '$' (Το νόμισμα είναι προαιρετικό)"]
        patient = self.get_patient_entry()
        fields = [patient.name, patient.age, patient.telephone,
                  patient.profession, patient.children, patient.price]
        entries = [self.name_entry, self.age_entry, self.telephone_entry,
                   self.profession_entry, self.children_entry, self.price_entry]
        functions = [patient.has_valid_name, patient.has_valid_age,
                     patient.has_valid_telephone, patient.has_valid_profession, patient.has_valid_children, patient.has_valid_price]
        for i in range(len(fields)):
            if not functions[i]():
                old_color = entries[i].cget("fg_color")
                entries[i].configure(fg_color="salmon")

                MessageBox("Σφάλμα", messages[i], "error")

                entries[i].configure(fg_color=old_color)

                return
        if patient.exists_in_database():

            MessageBox(
                "Σφάλμα", f"O θεραπευόμενος με όνομα '{patient.name}' και τηλέφωνο '{patient.telephone}' υπάρχει ήδη στη βάση δεδομένων.", "error")

        else:

            # If the data is valid and there is no duplicate entry in the database,
            # then we write to the database and create a folder for the patient

            try:
                patient.write_to_database()
            except (Error, DatabaseError, OperationalError) as exp:

                MessageBox(
                    "Σφάλμα", f"Παρουσιάστηκε σφάλμα κατά την εγγραφή στη βάση δεδομένων {exp}", "error")

                return

            try:

                patient.create_folder()

                patient.copy_files_to_folder(self.files)
            except (FileExistsError, PermissionError, FileNotFoundError, OSError, ValueError) as exp:

                MessageBox(
                    "Σφάλμα", f"Πραγματοποιήθηκε εγγραφή στη βάση δεδομένων.Στη συνέχεια παρουσιάστηκε σφάλμα κατά την δημιουργία φακέλου: {exp}", "error")

                return

            MessageBox(
                "Επιτυχία", f"Ο θεραπευόμενος με όνομα '{patient.name}' και τηλέφωνο '{patient.telephone}' καταχωρήθηκε επιτυχώς.", "success")
            self.clear_entries()
            self.manager.update_tables("patients")

    def attach_file(self):
        """Opens a file dialog and appends the selected file to the files list"""
        modal_window = tk.Toplevel(self)
        modal_window.withdraw()  # Hide the modal window

        # Make the modal window modal, disabling the parent window
        modal_window.grab_set()
        filenames = filedialog.askopenfilenames(
            initialdir="/", title="Select files", filetypes=(("All Files", "*.*"),), multiple=True)
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

    def grid_widgets(self):
        """Packs all the widgets in the frame"""

        for i, attribute in enumerate(self.attributes):
            for j, element in enumerate(attribute):
                if element == self.submit_button:
                    element.grid(row=i, column=1, padx=8, pady=5)
                elif element == self.attach_file_button:
                    element.grid(row=i, column=j, padx=8,
                                 pady=5)

                elif element == self.attach_file_clear_button:
                    element.grid(row=i, column=j, padx=2,
                                 pady=5, sticky='w')
                elif element == self.title_label:
                    element.grid(row=i, column=0, columnspan=2,
                                 padx=8, pady=5)

                else:
                    element.grid(row=i, column=j, padx=8,
                                 pady=5, sticky='nsew')

    def on_close(self):
        """Destroys the window and sets the master state to normal"""
        self.master.state('normal')
        self.grab_release()

        self.destroy()

    def test_fonts(self):
        """Test"""
        input_font = ["Bahnschrift Light", "Bahnschrift SemiLight", "Bahnschrift", "Bahnschrift SemiBold", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiLight SemiConde", "Bahnschrift SemiCondensed", "Bahnschrift SemiBold SemiConden", "Bahnschrift Light Condensed", "Bahnschrift SemiLight Condensed", "Bahnschrift Condensed", "Bahnschrift SemiBold Condensed", "Corbel", "Corbel Light", "Ink Free", "Malgun Gothic", "@Malgun Gothic", "Malgun Gothic Semilight", "@Malgun Gothic Semilight", "Microsoft Himalaya", "Microsoft JhengHei", "@Microsoft JhengHei", "Microsoft JhengHei UI", "@Microsoft JhengHei UI", "Microsoft JhengHei Light", "@Microsoft JhengHei Light", "Microsoft JhengHei UI Light", "@Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", "Microsoft Tai Le", "Microsoft YaHei", "@Microsoft YaHei", "Microsoft YaHei UI", "@Microsoft YaHei UI", "Microsoft YaHei Light", "@Microsoft YaHei Light", "Microsoft YaHei UI Light", "@Microsoft YaHei UI Light", "Microsoft Yi Baiti", "MingLiU-ExtB", "@MingLiU-ExtB", "PMingLiU-ExtB", "@PMingLiU-ExtB", "MingLiU_HKSCS-ExtB", "@MingLiU_HKSCS-ExtB", "Mongolian Baiti", "MS Gothic", "@MS Gothic", "MS UI Gothic",
                      "@MS UI Gothic", "MS PGothic", "@MS PGothic", "Verdana", "Yu Gothic", "@Yu Gothic", "Yu Gothic UI", "@Yu Gothic UI", "Yu Gothic UI Semibold", "@Yu Gothic UI Semibold", "Yu Gothic Light", "@Yu Gothic Light", "Yu Gothic UI Light", "@Yu Gothic UI Light", "Yu Gothic Medium", "@Yu Gothic Medium", "Yu Gothic UI Semilight", "@Yu Gothic UI Semilight", "HoloLens MDL2 Assets", "Cascadia Code ExtraLight", "Cascadia Code Light", "Cascadia Code SemiLight", "Cascadia Code", "Cascadia Code SemiBold", "Cascadia Mono ExtraLight", "Cascadia Mono Light", "Cascadia Mono SemiLight", "Cascadia Mono", "Cascadia Mono SemiBold"]

        self.myfont = customtkinter.CTkFont(
            family=input_font[1], size=24)

    def set_patient_entry(self, patient):
        """Sets the patient entry form to the values of the patient object passed in"""
        self.name_entry.insert('end', patient.name)
        self.session_type_combobox.set(patient.session_type)
        self.start_date_entry.insert('end', patient.start_date)
        self.referenced_by_entry.insert('end', patient.referenced_by)
        self.age_entry.insert('end', patient.age)
        self.telephone_entry.insert('end', patient.telephone)
        self.emergency_phone_entry.insert('end', patient.emergency_phone)
        self.address_entry.insert('end', patient.address)
        self.profession_entry.insert('end', patient.profession)
        self.marital_status_combobox.set(patient.marital_status)
        self.children_entry.insert('end', patient.children)
        self.medical_diagnosis_entry.insert('end', patient.medical_diagnosis)
        self.medical_prescription_entry.insert(
            'end', patient.medical_prescription)
        self.request_entry.insert('end', patient.request)
        self.price_entry.insert('end', patient.price)

    def get_patient_entry(self):
        """Gets the entered values from the patient entry form, removing any trailing whitespace"""
        new_patient = Patient()
        new_patient.name = self.name_entry.get().strip()
        new_patient.session_type = self.session_type_combobox.get().strip()
        new_patient.start_date = self.start_date_entry.get().strip()
        new_patient.referenced_by = self.referenced_by_entry.get().strip()
        new_patient.age = self.age_entry.get().strip()
        new_patient.telephone = self.telephone_entry.get().strip()
        new_patient.emergency_phone = self.emergency_phone_entry.get().strip()
        new_patient.address = self.address_entry.get().strip()
        new_patient.profession = self.profession_entry.get().strip()
        new_patient.marital_status = self.marital_status_combobox.get().strip()
        new_patient.children = self.children_entry.get().strip()
        new_patient.medical_diagnosis = self.medical_diagnosis_entry.get().strip()
        new_patient.medical_prescription = self.medical_prescription_entry.get().strip()
        new_patient.request = self.request_entry.get("0.0", "end").strip()
        new_patient.price = self.price_entry.get().strip()
        new_patient.active = 1  # By default the patient is active
        new_patient.attached_files = self.files

        return new_patient


if __name__ == '__main__':
    root = customtkinter.CTk()
    msg_box = MessageBox("Δοκιμή", "Αυτότό είναιΑυτό είναι ένα μήνυμα Αυτό Αυτό είναι ένα μήνυμα Αυτό είναι ένα μήνυμα δοκιμής δοκιμής είναι ένα μήνυμα ένα μήνυμα Αυτό είναι ένα μήνυμα δοκιμής δοκιμής είναι ένα μήνυμα Αυτό είναι ένα μήνυμα δοκιμής δοκιμής είναι ένα μήνυμα δοκιμής δοκιμής", option='success')

    # for i in range(80):

    #     newpatient_window = NewPatientGUI(root, customtkinter.CTkFont(
    #         family='Bahnschrift SemiLight', size=24))

    #     random_patient = RandomPatient()
    #     newpatient_window.set_patient_entry(random_patient)
    #     newpatient_window.on_submit()
    root.mainloop()
