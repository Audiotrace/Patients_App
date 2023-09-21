"""
This module contains the Patient class, which represents a patient in a medical system.
The Patient class has various attributes that store information about the patient,
such as their name, age,and medical history.
To use this module, simply import the Patient class and create instances of it with
the desired values for each attribute.
"""

import shutil
import sqlite3
import os

from datetime import datetime, time

import pytz


class Patient:
    """
    A class representing a patient.

    Attributes:
    - name (str): the name of the patient
    - session_type (str): can be internet, phone or in-person
    - start_date (str): the date the patient's sessions started
    - referenced_by (str): the name of the person/entity who referred the patient
    - age (str): the age of the patient
    - telephone (str): the telephone number of the patient
    - emergency_phone (str): the emergency telephone number of the patient
    - address (str): the address of the patient
    - profession (str): the profession of the patient
    - marital_status (str): the marital status of the patient
    - children ([]): A list containing the ages of the patient's children
    - medical_diagnosis (str): the medical diagnosis of the patient
    - medical_prescription (str): the medical prescription of the patient
    - request (str): the request of the patient
    - price (str): the price of the patient's session
    - attached_files ([]): A list containing the names of the attached files
    - unique_id (str): the unique ID of the patient
    - active (int): 1 if the patient is active, 0 otherwise
    """

    def __init__(self, name="",
                 session_type="",
                 start_date="",
                 referenced_by="",
                 age="",
                 telephone="",
                 emergency_phone="",
                 address="",
                 profession="",
                 marital_status="",
                 children="",
                 medical_diagnosis="",
                 medical_prescription="",
                 request="",
                 price="",
                 attached_files="",
                 folder_name="",
                 unique_id=None,
                 active=1):

        self.name = name
        self.session_type = session_type
        self.start_date = start_date
        self.referenced_by = referenced_by
        self.age = age
        self.telephone = telephone
        self.emergency_phone = emergency_phone
        self.address = address
        self.profession = profession
        self.marital_status = marital_status
        self.children = children
        self.medical_diagnosis = medical_diagnosis
        self.medical_prescription = medical_prescription
        self.request = request
        self.price = price
        self.attached_files = attached_files
        self.folder_name = folder_name
        self.unique_id = unique_id
        self.active = active

    def __str__(self):
        return f"""        Name: {self.name}
        Session type: {self.session_type}
        Start date: {self.start_date}
        Referenced by: {self.referenced_by}
        Age: {self.age}
        Telephone: {self.telephone}
        Emergency phone: {self.emergency_phone}
        Address: {self.address}
        Profession: {self.profession}
        Marital status: {self.marital_status}
        Children: {self.children}
        Medical diagnosis: {self.medical_diagnosis}
        Medical prescription: {self.medical_prescription}
        Request: {self.request}
        Price: {self.price}
        Attached files: {self.attached_files}
        Folder name: {self.folder_name}
        Unique ID: {self.unique_id}
        Active: {self.active}"""

    def to_dict(self):
        """Returns a dictionary containing
      the patient's attributes"""

        return {
            "name": self.name,
            "session_type": self.session_type,
            "start_date": self.start_date,
            "referenced_by": self.referenced_by,
            "age": self.age,
            "telephone": self.telephone,
            "emergency_phone": self.emergency_phone,
            "address": self.address,
            "profession": self.profession,
            "marital_status": self.marital_status,
            "children": self.children,
            "medical_diagnosis": self.medical_diagnosis,
            "medical_prescription": self.medical_prescription,
            "request": self.request,
            "price": self.price,
            "attached_files": self.attached_files,
            "folder_name": self.folder_name,
            "unique id": self.unique_id,
            "active": self.active
        }

    def get_name(self):
        """Returns the patient's name"""
        return self.name

    def get_price(self) -> str:
        """Returns the patient's price"""
        return self.price

    def has_valid_name(self):
        """Returns True if the patient's name is valid, False otherwise"""

        if len(self.name.split()) < 2 or self.name == "" or any(char in """¨©¬¥«»΅€®²³£§¶¤¦°±½½1234567890!"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.name):
            return False

        return True

    def has_valid_telephone(self):
        """Returns True if the patient's telephone number is valid, False otherwise"""
        if self.telephone == "" or any(char in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏ¨©¬¥«»΅€®²³£§¶¤¦°±½½!"#$%&\'()*,-./:;<=>@[\\]^_`{|}~΄""" for char in self.telephone):
            return False

        return True

    def has_valid_children(self):
        """Returns True if the patient's children field is valid, False otherwise"""

        if any(char in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏ¨©¬¥«»΅€®²³£§¶¤¦°±½½!"#$%&\'()*-./:;<=>@[\\]^_`{|}~΄""" for char in self.children):
            return False
        else:
            return True

    def has_valid_profession(self):
        """Returns True if the patient's profession field is valid, False otherwise"""
        if self.profession == "" or any(char in """¨©¬¥«»΅€®²³£§¶¤¦°±½½1234567890!"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.profession):
            return False
        else:
            return True

    def has_valid_age(self):
        """Returns True if the patient's age field is valid, False otherwise"""
        if self.age == "" or any(char in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏ¨©¬¥«»΅€®²³£§¶¤¦°±½½!"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.age):
            return False
        else:
            return True

    def has_valid_price(self):
        """Returns True if the patient's price field is valid, False otherwise"""
        if self.price == "" or any(char in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏ¨©¬¥«»΅®²³§¶¤¦°±½½!"#%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.price):
            return False
        else:
            return True

    def write_to_database(self):
        """Writes the patient's data to the database"""
        if self.start_date == "":
            self.start_date = "01/01/1900"
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        # Insert the patient's information into the database
        query = query = '''INSERT INTO patients ("Name", "Default Session Type","Start Date", "Referenced By", "Age", "Telephone", "Emergency Telephone", "Address", "Profession", "Marital Status", "Children", "Medical Diagnosis", "Medical Prescription", "Request", "Price","Folder Name","Active") VALUES (?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)'''

        values = (self.name,
                  self.session_type,
                  self.start_date,
                  self.referenced_by,
                  self.age,
                  self.telephone,
                  self.emergency_phone,
                  self.address,
                  self.profession,
                  self.marital_status,
                  self.children,
                  self.medical_diagnosis,
                  self.medical_prescription,
                  self.request,

                  self.price,

                  self.folder_name,
                  self.active
                  )

        cursor.execute(query, values)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def update_patient(self, patient_id):
        """Updates the patient's data in the database"""

        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        # Update the patient's information in the database
        query = '''UPDATE patients SET
                    "Name" = ?,
                    "Default Session Type" = ?,
                    "Start Date" = ?,
                    "Referenced By" = ?,
                    "Age" = ?,
                    "Telephone" = ?,
                    "Emergency Telephone" = ?,
                    "Address" = ?,
                    "Profession" = ?,
                    "Marital Status" = ?,
                    "Children" = ?,
                    "Medical Diagnosis" = ?,
                    "Medical Prescription" = ?,
                    "Request" = ?,
                    "Price" = ?,
                    "Active" = ?

                    WHERE "ID" = ?'''

        values = (self.name,
                  self.session_type,
                  self.start_date,
                  self.referenced_by,
                  self.age,
                  self.telephone,
                  self.emergency_phone,
                  self.address,
                  self.profession,
                  self.marital_status,
                  self.children,
                  self.medical_diagnosis,
                  self.medical_prescription,
                  self.request,
                  self.price,
                  self.active,
                  patient_id
                  )

        cursor.execute(query, values)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    @staticmethod
    def write_many_to_database(patients_list):
        """Writes a list of patients to the database"""
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()
        # Insert the patient's information into the database
        query = '''INSERT INTO patients ("Name", "Default Session Type","Start Date", "Referenced By", "Age", "Telephone", "Emergency Telephone", "Address", "Profession", "Marital Status", "Children", "Medical Diagnosis", "Medical Prescription", "Request", "Price","Folder Name","Active") VALUES (?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)'''
        for patient in patients_list:

            values = (patient.name,
                      patient.session_type,
                      patient.start_date,
                      patient.referenced_by,
                      patient.age,
                      patient.telephone,
                      patient.emergency_phone,
                      patient.address,
                      patient.profession,
                      patient.marital_status,
                      patient.children,
                      patient.medical_diagnosis,
                      patient.medical_prescription,
                      patient.request,

                      patient.price,

                      patient.folder_name,
                      patient.active
                      )

            cursor.execute(query, values)

            # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def open_folder(self):
        """Opens the patient's folder"""
        # print(
        #     f"folder_name inside open_folder:{self.folder_name}")

        directory_contents = os.listdir(os.path.dirname(self.folder_name))

        os.startfile(self.folder_name.replace('/', '\\'))

    def create_folder(self):
        """Creates a folder for the patient. Needs to be called after write_to_database()
        because it needs the patient's id from the database to create a unique folder name"""

        if self.exists_in_database():
            conn = sqlite3.connect("REAL_patients - Copy.db")
            cursor = conn.cursor()

            query = "SELECT id FROM patients WHERE name = ? AND telephone = ?"
            cursor.execute(query, (self.name, self.telephone))

            id_with_parenthesis = str(cursor.fetchone()).replace(',', '')

            conn.close()

            name_parts = self.name.split()
            name_parts.reverse()
            base_folder = "Φάκελοι Θεραπευόμενων"
            os.makedirs(base_folder, exist_ok=True)
            self.folder_name = f'{base_folder}/{" ".join(name_parts)} {self.age} {id_with_parenthesis}'
            self.unique_id = id_with_parenthesis.replace(
                '(', '').replace(')', '')

            if not os.path.exists(self.folder_name):
                os.makedirs(self.folder_name, exist_ok=True)

                # now update the database entry with the folder name
                conn = sqlite3.connect("REAL_patients - Copy.db")
                cursor = conn.cursor()
                query = 'UPDATE patients SET "Folder Name" = ? WHERE id = ?'
                cursor.execute(query, (self.folder_name, self.unique_id))

                conn.commit()
                conn.close()
            return
        # This code is executed if the patient doesn't exist in the database.
        # At this point a patient SHOULD exist in the database, but if it doesn't
        # we need to raise an error
        raise ValueError("create_folder(self) generated an error.")

    def copy_files_to_folder(self, files_to_add):
        """Updates the patient's folder with new files"""
        file_already_exists = []
        file_copied = []
        self.folder_name = self.folder_name.replace('/', '\\')
        for file_path in files_to_add:
            file = os.path.basename(file_path)
            if file not in os.listdir(self.folder_name):
                shutil.copy(file_path, self.folder_name)
                # print(f"file:{file}")

                # print(os.listdir(self.folder_name))
                file_copied.append('-'+file+'\n')

            else:
                file_already_exists.append('-'+file+'\n')

        string_files_copied = ''
        for file in file_copied:
            string_files_copied += file

        string_files_already_exists = ''
        for file in file_already_exists:
            string_files_already_exists += file

        if len(file_already_exists) == 1:
            omikron_or_alpha1 = 'ο'
            end1 = 'ει'
        else:
            omikron_or_alpha1 = 'α'
            end1 = 'ουν'

        if len(file_copied) == 1:
            omikron_or_alpha2 = 'ο'
            end2 = 'ε'
        else:
            omikron_or_alpha2 = 'α'
            end2 = 'αν'

        if file_already_exists and file_copied:
            raise FileExistsError(
                f"Τ{omikron_or_alpha1} παρακάτω αρχεί{omikron_or_alpha1}:\n{string_files_already_exists} υπάρχ{end1} ήδη στον φάκελο του θεραπευόμενου.\n T{omikron_or_alpha2} αρχεί{omikron_or_alpha2}:\n {string_files_copied} αντιγράφηκ{end2} με επιτυχία.")
        elif file_already_exists:
            raise FileExistsError(
                f"Τ{omikron_or_alpha1} παρακάτω αρχεί{omikron_or_alpha1}:\n{string_files_already_exists} υπάρχ{end1} ήδη στον φάκελο του θεραπευόμενου.")

    def exists_in_database(self):
        """Returns True if the patient exists in the database, False otherwise"""
        # connect to the database
        conn = sqlite3.connect('REAL_patients - Copy.db')

        # create a cursor
        curs = conn.cursor()

        # execute a SELECT query to check if the entry exists
        curs.execute("SELECT * FROM patients WHERE Name = ?", (self.name,))
        rows = curs.fetchall()

        # if no entry with the same name exists, return False
        if len(rows) == 0:
            conn.close()

            return False
        elif len(rows) == 1:
            return True

        # check the telephone field for each row with the same name
        for row in rows:
            if row[5] == self.telephone:
                conn.close()

                return True

        # close the connection
        conn.close()

        # if no matching entry is found, return False

        return False

# Useful for viewing the patient's data from the database

    def get_values_from_database_based_on_id(self, id_number=None):
        """Returns a list with the patient's data from the database"""
        if self.unique_id is None and id_number is None:
            raise ValueError(
                "id_number for patient not set")
        elif id_number is not None:
            self.unique_id = id_number
        # connect to the database
        conn = sqlite3.connect('REAL_patients - Copy.db')

        # create a cursor
        curs = conn.cursor()

        # execute a SELECT query to check if the entry exists
        curs.execute("SELECT * FROM patients WHERE id = ? ",
                     (self.unique_id,))

        # fetch the data
        rows = curs.fetchall()

        # close the connection
        conn.close()

        # get the patient's data
        self.name = rows[0][0]
        self.session_type = rows[0][1]
        self.start_date = rows[0][2]
        self.referenced_by = rows[0][3]
        self.age = rows[0][4]
        self.telephone = rows[0][5]
        self.emergency_phone = rows[0][6]
        self.address = rows[0][7]
        self.profession = rows[0][8]
        self.marital_status = rows[0][9]
        self.children = rows[0][10]
        self.medical_diagnosis = rows[0][11]
        self.medical_prescription = rows[0][12]
        self.request = rows[0][13]
        self.price = rows[0][14]
        self.folder_name = rows[0][15]
        self.unique_id = rows[0][16]
        # 17, and 18 are created at and modified at which
        # are set automatically by the database
        self.active = rows[0][19]

    def get_values_from_database_based_on_name(self):
        """Returns a list with the patient's data from the database"""
        # connect to the database
        conn = sqlite3.connect('REAL_patients - Copy.db')

        # create a cursor
        curs = conn.cursor()

        # execute a SELECT query to check if the entry exists
        curs.execute("SELECT * FROM patients WHERE Name = ? ",
                     (self.name,))

        # fetch the data
        rows = curs.fetchall()

        # close the connection
        conn.close()
        if len(rows) == 0:
            raise ValueError(
                f"Δεν υπάρχει θεραπευόμενος με το όνομα {self.name} στη βάση δεδομένων.")
        # get the patient's data
        self.name = rows[0][0]
        self.session_type = rows[0][1]
        self.start_date = rows[0][2]
        self.referenced_by = rows[0][3]
        self.age = rows[0][4]
        self.telephone = rows[0][5]
        self.emergency_phone = rows[0][6]
        self.address = rows[0][7]
        self.profession = rows[0][8]
        self.marital_status = rows[0][9]
        self.children = rows[0][10]
        self.medical_diagnosis = rows[0][11]
        self.medical_prescription = rows[0][12]
        self.request = rows[0][13]
        self.price = rows[0][14]
        self.folder_name = rows[0][15]
        self.unique_id = rows[0][16]
        # 17, and 18 are created at and modified at which
        # are set automatically by the database
        self.active = rows[0][19]

    def get_sessions_from_database(self, start_date, end_date):
        """Gets the lessons from the database"""

        start_date = self.convert_date_to_iso(start_date, "start")

        end_date = self.convert_date_to_iso(end_date, "end")
        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()
            # update the lessons table
            query = """SELECT * FROM Sessions WHERE datetime(Datetime) >= datetime(?) AND datetime(Datetime)<=datetime(?) AND Patient = ?;"""

            values = (start_date, end_date, self.name,)
            cursor.execute(query, values)
            sessions = cursor.fetchall()
            conn.close()

            return sessions
        # The returned sessions are not neccessarily in time order.
        # They are in entry order!
        finally:
            if conn:
                conn.close()

    def get_last_session_from_database(self):
        """Gets the last session from the database"""

        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()
            # update the lessons table
            query = """SELECT * FROM Sessions WHERE Patient = ? ORDER BY Datetime DESC LIMIT 1;"""

            values = (self.name,)
            cursor.execute(query, values)
            session = cursor.fetchone()
            conn.close()

            return session

        finally:
            if conn:
                conn.close()

    @staticmethod
    def convert_date_to_iso(date, time_marker=None):
        now = date.upper() == "NOW"
        if date.upper() == "TODAY":
            date = datetime.now().strftime("%d/%m/%Y")
        elif now:
            date = datetime.now().replace(microsecond=0)

        if not now:
            date = datetime.strptime(date, "%d/%m/%Y")
            time_object = {"start": time(0, 0, 0), "end": time(
                23, 59, 59)}.get(time_marker)
            if time_object is None:
                raise ValueError(
                    "Invalid time_marker. Valid options are 'start' or 'end'.")
            date = date.replace(
                hour=time_object.hour, minute=time_object.minute, second=time_object.second)

        localized_datetime = pytz.timezone("Europe/Athens").localize(date)
        return localized_datetime.isoformat()


if __name__ == "__main__":
    test_patient = Patient()
    test_patient.get_values_from_database(107)
    print(test_patient)
    test_patient.create_folder()
