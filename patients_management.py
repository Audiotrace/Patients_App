"""This module contains the sessionsManagement class"""
from datetime import datetime, timedelta
import threading
import json
from winsound import SND_FILENAME, PlaySound
from new_session_gui import NewSessionGUI

from patients_management_database import PatientsDatabase, SessionsDatabase, GeneralDatabase
from sessions_calendar import SessionsCalendar
from statistics_panel import StatisticsPanel
from tdamourakis_ctkinter import MessageBox
import customtkinter
from greek_language import GreekLanguage
from random import randint, choice

import os
from PIL import Image
from new_patient_gui import NewPatientGUI
from patients_management_tables import PatientsTable, SessionsTable, UnconfirmedSessionsTable, IgnoredEventsTable


class PatientsManagement(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.idx = 0
        self.patients = []
        self.sessions = []
        self.patients_names_set = set()
        self.unconfirmed_sessions = []
        self.title("Διαχείριση Συνεδριών")
        self.geometry("1200x700")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.set_fonts()
        self.initialize_dates()
        self.set_grid_layout()
        self.load_images()
        self.show_inactive_sessions = True
        self.show_inactive_patients = True
        self.create_main_frames()
        self.create_basic_menu_widgets()
        self.grid_basic_menu_widgets()
        # select default frame
        self.select_frame_by_name("home")
        self.statistics_panel = StatisticsPanel(self.view_sessions_frame)
        self.create_home_loading_frame()
        self.create_tables()
        self.update_idletasks()
        self.after(100, self.initialize_data)
        self.new_session_gui = NewSessionGUI(
            self.add_new_session_frame, self, myfont=self.main_font)
        self.new_patient_gui = NewPatientGUI(
            self.add_new_patient_frame, manager=self,  myfont=self.main_font)
        self.create_info_frame_for_patients()
        self.create_buttons_frame_for_unconfirmed_sessions()
        customtkinter.set_appearance_mode("light")
        self.image_label = customtkinter.CTkLabel(
            self.home_frame, fg_color="transparent", text="")
        self.quote_label = customtkinter.CTkLabel(
            self.home_frame, text="", font=("Bahnschrift SemiLight Bold", 24), fg_color="transparent")
        self.after(1000, self.check_connection_periodically)

    def create_buttons_frame_for_unconfirmed_sessions(self):
        self.unconfirmed_sessions_buttons_frame = customtkinter.CTkFrame(
            self.verify_sessions_frame, corner_radius=10, fg_color="transparent")
        self.get_unconfirmed_events_button = customtkinter.CTkButton(self.unconfirmed_sessions_buttons_frame, text="Αναζήτηση",
                                                                     command=self.get_unconfirmed_events_button_event, font=self.main_font, height=65)
        self.show_ignored_events_button = customtkinter.CTkButton(self.unconfirmed_sessions_buttons_frame, text="Προβολή λίστας αγνοημένων",
                                                                  command=self.get_ignored_events_button_event, font=self.main_font, height=65, width=360)
        self.start_date_label = customtkinter.CTkLabel(
            self.unconfirmed_sessions_buttons_frame, text="Από:", font=self.main_font)
        self.start_date_entry = customtkinter.CTkEntry(
            self.unconfirmed_sessions_buttons_frame, width=200, font=self.main_font, placeholder_text="dd/mm/yyyy")
        self.start_date_entry.insert(0, self.start_date_of_events)
        self.end_date_label = customtkinter.CTkLabel(
            self.unconfirmed_sessions_buttons_frame, text="Έως:", font=self.main_font)
        self.end_date_entry = customtkinter.CTkEntry(
            self.unconfirmed_sessions_buttons_frame, width=200, font=self.main_font)
        self.end_date_entry.insert(0, self.today)
        self.start_date_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.end_date_label.grid(row=1, column=0, padx=10, pady=10)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)
        self.show_ignored_events_button.grid(
            row=0, column=4, rowspan=2, padx=(400, 10), pady=10)
        self.get_unconfirmed_events_button.grid(
            row=0, column=2, rowspan=2, padx=10, pady=10)
        self.unconfirmed_sessions_info_label = customtkinter.CTkLabel(
            self.unconfirmed_sessions_buttons_frame, text="", font=self.main_font)
        self.unconfirmed_sessions_info_label.grid(
            row=2, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        self.unconfirmed_sessions_buttons_frame.pack(
            expand=False, fill="x", side='top', padx=10, pady=10)

    def create_info_frame_for_patients(self):
        self.patients_info_frame = customtkinter.CTkFrame(
            self.view_patients_frame, corner_radius=10, fg_color="transparent")
        self.patients_info_label = customtkinter.CTkLabel(
            self.patients_info_frame, text="", font=self.main_font)
        self.patients_info_label.pack(
            expand=False, fill="x", side='top', padx=10, pady=10)
        self.patients_info_frame.pack(
            expand=False, fill="x", side='top', padx=10, pady=10)
        # Create checkbox for enabling/disabling inactive patients
        self.active_patients_checkbox = customtkinter.CTkCheckBox(
            self.patients_info_frame, text="Εμφάνιση Ανενεργών", command=self.update_inactive_attribute)
        self.active_patients_checkbox.toggle()
        self.active_patients_checkbox.pack(
            expand=False, fill="x", side='top', padx=10, pady=10)

    def create_home_loading_frame(self):
        self.loading_frame = customtkinter.CTkFrame(
            self.home_frame, corner_radius=10, fg_color="transparent")
        self.loading_frame.pack(expand=True, fill="both")
        self.progress_bar = customtkinter.CTkProgressBar(
            master=self.loading_frame, mode="indeterminate")

        self.loading_label = customtkinter.CTkLabel(
            self.loading_frame, text="", font=("Bahnschrift SemiLight Bold", 34))

        self.loading_label.pack(expand=False, fill="x",
                                anchor='center', pady=(350, 10))
        self.progress_bar.pack(
            expand=False, fill="both", anchor='center', pady=20)

    def initialize_dates(self):

        self.today = datetime.now().date()
        self.start_date_of_events = self.today - timedelta(weeks=1)
        self.today = self.today.strftime("%d/%m/%Y")
        self.start_date_of_events = self.start_date_of_events.strftime(
            "%d/%m/%Y")

    def initialize_data(self):

        initialization_thread = threading.Thread(
            target=self._initialize_data_in_new_thread)
        initialization_thread.start()

        self.progress_bar.start()
        self.after(500, self.check_thread, initialization_thread)
        self.loading_label.configure(text="Φόρτωση δεδομένων...")

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(1000, self.check_thread, thread)
        else:

            self._post_thread_initialization()

    def _initialize_data_in_new_thread(self):
        self.patients = PatientsDatabase.get_patients_as_list_of_strings(
            inactive=self.show_inactive_patients)
        self.sessions = SessionsDatabase.get_sessions_as_list_of_strings(
            inactive=self.show_inactive_sessions)
        self.patients_names_set = {row[0] for row in self.patients}
        self.calendar = SessionsCalendar()

        self.unconfirmed_sessions = self.calendar.filter_events(self.calendar.get_events(
            self.start_date_of_events, self.today))

    def _post_thread_initialization(self):

        self.patients_table.set_data(self.patients)
        self.sessions_table_for_new_session_gui.set_data(self.sessions)
        self.sessions_table_for_view_sessions.set_data(self.sessions)

        self.loading_label.configure(text="Φόρτωση Ραντεβού...")
        self.update()

        self.unconfirmed_sessions_table.set_data(
            self.unconfirmed_sessions, reset_scroll=False)
        self.loading_label.configure(text="Ολοκληρώθηκε!")
        self.update()
        self.update_unconfirmed_sessions_info_label()

        self.loading_frame.destroy()

        today = datetime.now()
        if today.month == 8 and today.day == 9:
            self.happy_birthday_label = customtkinter.CTkLabel(
                self.home_frame, text="", image=self.happy_birthday_image)
            self.happy_birthday_label.pack(expand=True, fill="both")
        else:
            rand_int = randint(0, len(self.home_images)-1)
            if rand_int in [0, 1, 2]:
                filename = "psy_quotes.json"
            elif rand_int in [3, 4, 5]:
                filename = "clever_quotes.json"
            self.image_label.configure(image=self.home_images[rand_int])

            self.image_label.pack(expand=True, fill="both", side='top')
            get_random_quote_thread = threading.Thread(
                target=self.get_random_quote, args=(filename, 100))
            get_random_quote_thread.start()

            self.quote_label.pack(expand=True, fill="both", side='bottom')
            if self.image_label.cget("image") == self.home_images[5]:
                sound_thread = threading.Thread(target=lambda: PlaySound(
                    'Sounds/cuckoo_clock.wav', SND_FILENAME))
                sound_thread.start()

    def get_random_quote(self, filename, max_line_length=100):
        # Open the file and load the quotes
        with open(filename, 'r') as f:
            quotes = json.load(f)

        # Choose a random quote
        random_quote = choice(quotes)
        quote = random_quote["quote"]

        # If the quote is too long, split it into two lines
        if len(quote) > max_line_length:
            midpoint = len(quote) // 2    # Find the midpoint of the string
            # Find a space near the midpoint
            split_point = quote.rfind(' ', 0, midpoint)

            # Split the quote into two lines at the split point
            quote = quote[:split_point] + '\n' + quote[split_point + 1:]

        # Format the quote and author
        quote_string = f'{quote} - {random_quote["author"]}'

        self.after(0, self.update_label_text, quote_string)

    def update_label_text(self, text):
        self.quote_label.configure(text=text)

    def update_unconfirmed_sessions_info_label(self):

        if not hasattr(self, "unconfirmed_sessions_table"):
            return
        number_of_events = len(self.unconfirmed_sessions_table.displayed_data)
        if number_of_events == 0:
            self.unconfirmed_sessions_info_label.configure(
                text=f"Αριθμός ραντεβού: 0")
            return

        unidentified = 0
        for row in self.unconfirmed_sessions_table.displayed_data:
            if row[3] == "":
                unidentified += 1

        if number_of_events == 1:
            self.unconfirmed_sessions_info_label.configure(
                text=f"Αριθμός ραντεβού: 1 {'(ταυτοποιημένο)' if unidentified == 0 else '(μη ταυτοποιημένο)'}")
            return
        if unidentified == 0:
            self.unconfirmed_sessions_info_label.configure(
                text=f"Αριθμός ραντεβού: {number_of_events}")
        else:
            text = f"εκ των οποίων {unidentified}" if unidentified < number_of_events else ", όλα"
            self.unconfirmed_sessions_info_label.configure(
                text=f"Αριθμός ραντεβού: {number_of_events} {text} χωρίς ταυτοποιημένο θεραπευόμενο.")

    def update_patients_info_label(self):

        if not hasattr(self, "patients_table"):
            return

        inactive = 0
        for row in self.patients_table.displayed_data:
            if row[7] == "0":
                inactive += 1
        if len(self.patients_table.displayed_data) == 0:
            self.patients_info_label.configure(
                text=f"Αριθμός θεραπευόμενων: 0")
            return
        if len(self.patients_table.displayed_data) == 1:
            self.patients_info_label.configure(
                text=f"Αριθμός θεραπευόμενων: 1 {'(ενεργός)' if inactive == 0 else '(μη ενεργός)'}")
            return
        if self.active_patients_checkbox.get() == 1:
            if 0 < inactive < 2:
                text = "ανενεργός"
                inactive_text = f"εκ των οποίων {inactive} {text}"
            elif inactive == 0:
                inactive_text = ""
            else:
                inactive_text = f"εκ των οποίων {inactive} ανενεργοί"
        else:
            inactive_text = ""
        self.patients_info_label.configure(
            text=f"Αριθμός θεραπευόμενων: {len(self.patients_table.displayed_data)} " + inactive_text)

    def identify_patient(self, unidentified_name: str) -> tuple:
        # The input string might have the format "Name Surname" or "Surname Name"
        # We also need to check for typos. We will use the levenshtein distance

        for patient in self.patients:

            distance = GreekLanguage.calculate_levenshtein_distance(
                patient[0], unidentified_name)
            if distance >= 4:
                continue
            if distance < 3:
                return (patient[0], distance)

        return ("unidentified", -1)

    def set_grid_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def set_fonts(self):
        self.title_font = customtkinter.CTkFont(
            family='Bahnschrift SemiLight Bold', size=24, weight="bold")
        self.main_font = customtkinter.CTkFont(
            family='Bahnschrift SemiLight Bold', size=18)

    def grid_basic_menu_widgets(self):

        self.navigation_frame_label.grid(
            row=0, column=0, padx=10, pady=10)

        self.home_button.grid(row=1, column=0, sticky="ew")
        self.verify_sessions_button.grid(row=2, column=0, sticky="ew")
        self.view_patients_button.grid(row=3, column=0, sticky="ew")
        self.view_sessions_button.grid(row=4, column=0, sticky="ew")
        self.add_new_session_button.grid(row=6, column=0, sticky="ew")
        self.add_new_Patient_button.grid(row=7, column=0, sticky="ew")

        self.navigation_frame.grid_rowconfigure(1, weight=1)
        self.navigation_frame.grid_rowconfigure(2, weight=1)
        self.navigation_frame.grid_rowconfigure(3, weight=1)
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame.grid_rowconfigure(5, weight=500)
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame.grid_rowconfigure(7, weight=1)
        self.navigation_frame.grid_rowconfigure(8, weight=1)
        self.navigation_frame.grid_rowconfigure(9, weight=1)

        self.appearance_mode_menu.grid(
            row=9, column=0, rowspan=20, padx=20, pady=20, sticky="w")

    def create_basic_menu_widgets(self):
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image,
                                                             compound="left", font=self.title_font)
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=5, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event, font=self.main_font)
        self.view_patients_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=10, text="Προβολή Θεραπευόμενων",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.view_patients_image, anchor="w", command=self.view_patients_button_event, font=self.main_font
        )
        self.view_sessions_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=10, text="Προβολή Συνεδριών",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.view_sessions_image, anchor="w", command=self.view_sessions_button_event, font=self.main_font
        )
        self.verify_sessions_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=10, text="Επιβεβαίωση Συνεδριών",
                                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                              image=self.confirm_sessions_image, anchor="w", command=self.verify_sessions_button_event, font=self.main_font)

        self.add_new_Patient_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=10, text="Νέος Θεραπευόμενος",
                                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                              image=self.add_new_patient_image, anchor="w", command=self.add_new_Patient_button_event, font=self.main_font)
        self.add_new_session_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, width=100, height=40, border_spacing=10, text="Νέα Συνεδρία",
                                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                              image=self.add_new_session_image, anchor="w", command=self.add_new_session_button_event, font=self.main_font)

    def create_tables(self):
        self.sessions_table_for_new_session_gui = SessionsTable(
            master=self.add_new_session_frame, manager=self)

        self.sessions_table_for_view_sessions = SessionsTable(
            master=self.view_sessions_frame, manager=self)

        self.patients_table = PatientsTable(
            master=self.view_patients_frame, manager=self)

        self.unconfirmed_sessions_table = UnconfirmedSessionsTable(
            self.verify_sessions_frame, manager=self)

    def create_main_frames(self):

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.navigation_frame.grid(
            row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=10, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # create verify sessions frame
        self.verify_sessions_frame = customtkinter.CTkFrame(
            self, corner_radius=10, fg_color="transparent")

        # create add new session frame
        self.add_new_session_frame = customtkinter.CTkFrame(
            self, corner_radius=10, fg_color="transparent")
        self.add_new_session_frame.grid_rowconfigure(0, weight=1)
        self.add_new_session_frame.grid_columnconfigure(0, weight=1)

        # create add new patient frame
        self.add_new_patient_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=10, fg_color="transparent", height=1500)

        # create view patients frame
        self.view_patients_frame = customtkinter.CTkFrame(
            self, corner_radius=10, fg_color="transparent")
        # create view sessions frame
        self.view_sessions_frame = customtkinter.CTkFrame(
            self, corner_radius=10, fg_color="transparent")

    def update_inactive_attribute(self):
        self.show_inactive_patients = self.active_patients_checkbox.get() == 1
        self.update_tables("patients")

    def get_unconfirmed_events_button_event(self):
        start_date_of_events = self.start_date_entry.get().strip()
        end_date_of_events = self.end_date_entry.get().strip()
        bad_start_date = False
        bad_end_date = False
        try:
            start_date_of_events = datetime.strptime(
                start_date_of_events, "%d/%m/%Y")
        except ValueError:
            bad_start_date = True

        if end_date_of_events == "":
            end_date_of_events = datetime.now()
        else:
            try:
                end_date_of_events = datetime.strptime(
                    end_date_of_events, "%d/%m/%Y")
            except ValueError:
                bad_end_date = True

        if bad_start_date:
            if bad_end_date:
                MessageBox(
                    "Σφάλμα", "Η ημερομηνία έναρξης δεν είναι έγκυρη.Οχι οτι η ημερομηνία λήξης παει πίσω...", "error")
                return
            else:
                MessageBox(
                    "Σφάλμα", "Η ημερομηνία έναρξης που δώσατε δεν είναι έγκυρη", "error")
                return

        if bad_end_date:
            MessageBox(
                "Σφάλμα", "Η ημερομηνία λήξης που δώσατε δεν είναι έγκυρη", "error")
            return

        if start_date_of_events > end_date_of_events:
            MessageBox(
                "Σφάλμα", "Η ημερομηνία έναρξης είναι μεταγενέστερη από την ημερομηνία λήξης", "error")
            return

        self.update_tables("unconfirmed_sessions",
                           start=start_date_of_events, end=end_date_of_events)

    def check_connection_periodically(self):

        if not hasattr(self, "calendar"):
            self.after(300, self.check_connection_periodically)
            print("Dont have calendar yet")
            return

        # Move the actual check to a separate thread
        check_thread = threading.Thread(
            target=self._check_connection_in_thread, daemon=True)
        check_thread.start()

        # schedule the next check in 10 seconds
        self.after(5000, self.check_connection_periodically)

    def _check_connection_in_thread(self):
        # This runs in a separate thread, but doesn't interact with tkinter directly
        if self.calendar.is_connected():
            image = self.confirm_sessions_image
            connected = True

        else:
            image = self.confirm_sessions_image_bw
            connected = False

        # Use tkinter's `after` to schedule the GUI update to run in the main thread
        self.after(3, self._update_verify_button, image, connected)

    def _update_verify_button(self, image, connected: bool):
        # This runs in the main thread and can safely interact with tkinter
        self.verify_sessions_button.configure(image=image)
        if not connected:
            self.verify_sessions_button.configure(
                text="!Επιβεβαίωση Συνεδριών")
        else:
            self.verify_sessions_button.configure(
                text="Επιβεβαίωση Συνεδριών")

    def get_ignored_events_button_event(self):
        top_level = customtkinter.CTkToplevel()
        top_level.title("Λίστα Αγνοημένων Συμβάντων")
        top_level.geometry("800x600")
        top_level.grab_set()
        top_level.focus_set()
        ignored_events_table = IgnoredEventsTable(
            top_level, manager=self)
        ignored_events_table.set_data(
            GeneralDatabase.get_ignored_events())
        ignored_events_table.pack(expand=True, fill="both", padx=10, pady=10)
        ignored_events_table.update_textboxes(event=None)

    def on_close(self):
        # self.master.state("normal")
        # self.grab_release()
        self.destroy()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.verify_sessions_button.configure(
            fg_color=("gray75", "gray25") if name == "verify_sessions" else "transparent")
        self.add_new_session_button.configure(
            fg_color=("gray75", "gray25") if name == "add_new_session" else "transparent")
        self.add_new_Patient_button.configure(
            fg_color=("gray75", "gray25") if name == "add_new_Patient" else "transparent")
        self.view_patients_button.configure(
            fg_color=("gray75", "gray25") if name == "view_patients" else "transparent")
        self.view_sessions_button.configure(
            fg_color=("gray75", "gray25") if name == "view_sessions" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "verify_sessions":
            self.verify_sessions_frame.grid(
                row=0, column=1, sticky="nsew")
        else:
            self.verify_sessions_frame.grid_forget()
        if name == "add_new_session":
            self.add_new_session_frame.grid(
                row=0, column=1, sticky="nsew", padx=20, pady=20)
        else:
            self.add_new_session_frame.grid_forget()
        if name == "add_new_Patient":
            self.add_new_patient_frame.grid(
                row=0, column=1, sticky="nsew", padx=20, pady=20)
        else:
            self.add_new_patient_frame.grid_forget()
        if name == "view_patients":
            self.view_patients_frame.grid(
                row=0, column=1, sticky="nsew", padx=20, pady=20
            )
        else:
            self.view_patients_frame.grid_forget()
        if name == "view_sessions":
            self.view_sessions_frame.grid(
                row=0, column=1, sticky="nsew", padx=20, pady=20
            )

        else:
            self.view_sessions_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def verify_sessions_button_event(self):

        self.select_frame_by_name("verify_sessions")
        if self.calendar.credentials is None or self.calendar.calendar_id is None:
            self.calendar = SessionsCalendar()
        self.unconfirmed_sessions_table.pack(
            expand=True, fill="both", padx=10, pady=20
        )

        self.unconfirmed_sessions_table.update_textboxes(event=None)

    def add_new_session_button_event(self):

        self.select_frame_by_name("add_new_session")

        self.new_session_gui.grid(
            row=0, column=0, sticky="ew", padx=10, pady=10)
        # Ensure sessions_table fills available space
        self.sessions_table_for_new_session_gui.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=20)

        self.sessions_table_for_new_session_gui.update_textboxes(event=None)

    def add_new_Patient_button_event(self):
        self.select_frame_by_name("add_new_Patient")
        # self.update_data(source=type(self.new_patient_gui))

        self.new_patient_gui.pack(fill='both', expand=True, padx=10, pady=10)

    def view_patients_button_event(self):
        self.select_frame_by_name("view_patients")
        self.active_patients_checkbox.pack(
            fill='none', expand=False, side='top', padx=10, pady=10)
        self.patients_table.pack(
            expand=True, fill="both", padx=10, pady=20)
        self.patients_table.update_textboxes(event=None)

    def view_sessions_button_event(self):

        self.select_frame_by_name("view_sessions")
        self.statistics_panel.pack(fill='x', expand=False, padx=10, pady=10)

        self.sessions_table_for_view_sessions.pack(
            expand=True, fill="both", padx=10, pady=20)
        self.sessions_table_for_view_sessions.update_textboxes(event=None)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            self.sessions_table_for_view_sessions.set_mode(mode="dark")
            self.sessions_table_for_new_session_gui.set_mode(mode="dark")
            self.unconfirmed_sessions_table.set_mode(mode="dark")
            self.patients_table.set_mode(mode="dark")
        elif new_appearance_mode == "Light":
            self.sessions_table_for_view_sessions.set_mode(mode="light")
            self.sessions_table_for_new_session_gui.set_mode(mode="light")
            self.unconfirmed_sessions_table.set_mode(mode="light")
            self.patients_table.set_mode(mode="light")

    def update_tables(self, target: str, start: datetime = None, end: datetime = None):

        if target == "sessions":
            self.sessions = SessionsDatabase.get_sessions_as_list_of_strings(
                inactive=self.show_inactive_sessions)
            self.sessions_table_for_new_session_gui.set_data(
                self.sessions, reset_scroll=False)
            self.sessions_table_for_view_sessions.set_data(
                self.sessions, reset_scroll=False)
        elif target == "patients":
            self.patients = PatientsDatabase.get_patients_as_list_of_strings(
                inactive=self.show_inactive_patients)
            self.patients_table.set_data(self.patients, reset_scroll=False)
        elif target == "unconfirmed_sessions":
            if self.calendar.credentials is None or self.calendar.calendar_id is None:
                self.calendar = SessionsCalendar()
            if end is None:
                if self.end_date_entry.get().strip() == "":
                    end = datetime.now()
                else:
                    try:
                        end = datetime.strptime(
                            self.end_date_entry.get().strip(), "%d/%m/%Y")
                    except ValueError:
                        end = datetime.now().strftime("%d/%m/%Y")
            if start is None:
                if self.start_date_entry.get().strip() == "":
                    start = end - timedelta(weeks=1)
                else:
                    try:
                        start = datetime.strptime(
                            self.start_date_entry.get().strip(), "%d/%m/%Y")
                    except ValueError:
                        start = end - timedelta(weeks=1)
            if self.calendar.is_connected():

                if start != end:
                    self.unconfirmed_sessions = self.calendar.filter_events(self.calendar.get_events(
                        start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y")))
                else:
                    self.unconfirmed_sessions = self.calendar.filter_events(self.calendar.get_events(
                        start.strftime("%d/%m/%Y")))
                self.unconfirmed_sessions_table.set_data(
                    self.unconfirmed_sessions, reset_scroll=False)
                self.update_unconfirmed_sessions_info_label()
            else:
                MessageBox(
                    "Σφάλμα", "Δεν υπάρχει σύνδεση με το διαδίκτυο.", "error")

    def update_stats(self):
        self.statistics_panel.calculate_stats(
            self.sessions_table_for_view_sessions.displayed_data)

    def load_images(self):
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "test images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(
            image_path, "cuckoo.ico")), size=(50, 50))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "cuckoo_home.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "cuckoo_home.png")), size=(40, 40))
        self.add_new_patient_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                            dark_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(30, 30))

        self.add_new_session_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                            dark_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(30, 30))
        self.confirm_sessions_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "google_logo.png")),
                                                             dark_image=Image.open(os.path.join(image_path, "google_logo.png")), size=(30, 30))
        self.view_patients_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "python_logo.png")),
                                                          dark_image=Image.open(os.path.join(image_path, "python_logo.png")), size=(30, 30))
        self.view_sessions_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "python_logo.png")),
                                                          dark_image=Image.open(os.path.join(image_path, "python_logo.png")), size=(30, 30))

        self.happy_birthday_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "HB.png")),
                                                           dark_image=Image.open(os.path.join(image_path, "HB.png")), size=(752, 587))
        self.confirm_sessions_image_bw = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "google_logo_bw.png")),
                                                                dark_image=Image.open(os.path.join(image_path, "google_logo_bw.png")), size=(30, 30))
        self.home_images = []

        # Read image information from JSON
        with open('home_screen_images.json') as json_file:
            data = json.load(json_file)
            for image_data in data['images']:
                image_name = image_data['name']
                image_file_path = image_data['image_path']
                image_size = image_data['size']

                image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, image_file_path)),
                                               dark_image=Image.open(os.path.join(image_path, image_file_path)), size=image_size)

                setattr(self, image_name, image)
                self.home_images.append(image)

    def on_unconfirmed_session_double_click(self, event=None):

        pass


if __name__ == '__main__':
    app = PatientsManagement()
    app.state('zoomed')
    app.mainloop()
