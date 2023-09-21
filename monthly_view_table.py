import time
from typing import List
from my_table import CustomTable
import customtkinter
from datetime import datetime
from patients_management_database import SessionsDatabase
from patient import Patient


class MonthlyViewTable(CustomTable):
    def __init__(self, master, data: List[List[str]], manager=None, **kwargs):
        self.month = self.inGreek(datetime.now().strftime("%B"))
        self.year = datetime.now().strftime("%Y")
        self.raw_data = data

        super().__init__(master, manager, heading_names=(
            "", "1", "2", "3", "4", "5", "Σύνολο"),
            column_widths=("250", "40", "40", "40", "40", "40", "130"),
            column_types=("name", "price", "price", "price", "price", "price", "price"), ** kwargs)
        self.disable_searchboxes()
        self.month_option_menu = customtkinter.CTkOptionMenu(
            self.searchboxes_frame, values=["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος",
                                            "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"],
            command=self.change_month)
        years = range(2020, int(self.year)+2)
        years = [str(year) for year in years]
        self.year_option_menu = customtkinter.CTkOptionMenu(
            self.searchboxes_frame, values=years, command=self.change_month)
        self.total_label = customtkinter.CTkLabel(
            self.searchboxes_frame, text="0€", font=(self.font_name, 18))
        self.total_label.pack(
            expand=False, fill="none", side='right', padx=20, pady=20)
        self.month_option_menu.set(self.month)
        self.year_option_menu.set(self.year)
        self.change_month(None)
        self.month_option_menu.pack(
            expand=False, fill="none", side='left', padx=20, pady=20)
        self.year_option_menu.pack(
            expand=False, fill="none", side='left', padx=20, pady=20)

        self.table.unbind("<Configure>")
        self.table.unbind("<Double-Button-1>")
        self.table.unbind("<Button-3>")

        for heading in self.heading_names:

            self.table.heading(heading, text=heading, anchor="center",
                               command=lambda: None)

    def fill_table(self, tags=['odd', 'even'], **kwargs):
        index = 0
        self.table.delete(*self.table.get_children())
        self.displayed_data = []
        for row in self.data_to_display:
            status = tags[index]
            if row[0] == "":
                status = "blank"
            self.table.insert('', 'end', values=row, tags=status)
            self.displayed_data.append(row)
            index = 1 - index

    def change_month(self, event):
        self.month = str(self.greek_month_to_int(self.month_option_menu.get()))
        self.year = self.year_option_menu.get()
        if len(self.month) < 2:
            self.month = "0" + self.month
        self.process_data(self.raw_data)

    def process_data(self, data):
        data.sort(key=lambda sublist: sublist[2].split(" ")[1])
        self.raw_data = data

        processed_data = []
        idx = 0
        processed_patients = {}
        for idx, row in enumerate(data):
            if row[0].split("/")[1] == self.month and row[0].split("/")[2] == self.year:
                if row[2] not in processed_patients.keys():
                    processed_patients[row[2]] = [
                        self.occurrence_of_day_in_month(row[0]),]
                else:
                    processed_patients[row[2]].append(
                        self.occurrence_of_day_in_month(row[0]))

            else:

                continue
        for patient in processed_patients:
            row = [patient, "", "", "", "", "", 0]
            for value in processed_patients[patient]:
                patient_obj = Patient(name=patient)
                patient_obj.get_values_from_database_based_on_name()
                row[value] = int(patient_obj.price)
                row[6] += int(patient_obj.price)
            processed_data.append(row)

        total = 0
        for row in processed_data:
            total += row[6]
        processed_data.append(["", "", "", "", "", "", ""])
        processed_data.append(["Σύνολο", "", "", "", "", "", total])
        self.set_data(processed_data)
        self.total_label.configure(text=str(total) + " €")

    def occurrence_of_day_in_month(self, date_str: str) -> int:
        # Parse the date string into a date object
        date_object = datetime.strptime(date_str, '%d/%m/%Y')

        # Calculate which occurrence of the day within the month
        day_occurrence = (date_object.day - 1) // 7 + 1

        return day_occurrence

    def inGreek(self, month: str) -> str:
        if not isinstance(month, str):
            raise TypeError("Month must be a string")
        month = month.upper()
        if month == "JANUARY" or month == "1":
            return "Ιανουάριος"
        elif month == "FEBRUARY" or month == "2":
            return "Φεβρουάριος"
        elif month == "MARCH" or month == "3":
            return "Μάρτιος"
        elif month == "APRIL" or month == "4":
            return "Απρίλιος"
        elif month == "MAY" or month == "5":
            return "Μάιος"
        elif month == "JUNE" or month == "6":
            return "Ιούνιος"
        elif month == "JULY" or month == "7":
            return "Ιούλιος"
        elif month == "AUGUST" or month == "8":
            return "Αύγουστος"
        elif month == "SEPTEMBER" or month == "9":
            return "Σεπτέμβριος"
        elif month == "OCTOBER" or month == "10":
            return "Οκτώβριος"
        elif month == "NOVEMBER" or month == "11":
            return "Νοέμβριος"
        elif month == "DECEMBER" or month == "12":
            return "Δεκέμβριος"
        else:
            raise ValueError("Invalid month")

    def greek_month_to_int(self, month: str) -> int:
        if not isinstance(month, str):
            raise TypeError("Month must be a string")
        value = 0
        if month == "Ιανουάριος":
            value = 1
        elif month == "Φεβρουάριος":
            value = 2
        elif month == "Μάρτιος":
            value = 3
        elif month == "Απρίλιος":
            value = 4
        elif month == "Μάιος":
            value = 5
        elif month == "Ιούνιος":
            value = 6
        elif month == "Ιούλιος":
            value = 7
        elif month == "Αύγουστος":
            value = 8
        elif month == "Σεπτέμβριος":
            value = 9
        elif month == "Οκτώβριος":
            value = 10
        elif month == "Νοέμβριος":
            value = 11
        elif month == "Δεκέμβριος":
            value = 12
        if not value:
            raise ValueError("Invalid Argument")
        return value


if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("800x600")
    sessions = SessionsDatabase.get_sessions_as_list_of_strings()
    table = MonthlyViewTable(root, data=sessions)

    table.pack(fill="y", expand=True)

    root.mainloop()
