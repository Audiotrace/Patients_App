"""
This module contains the patient class, which represents a patient.
The patient class has various attributes that store information about the patient,
such as their name, age, etc

"""

import random
import sqlite3

from datetime import datetime

import pytz

from patient import Patient


class Session:
    """Represents a Session"""

    def __init__(self, patient_instance: Patient, date_time=None, price=None,  paid=1, receipt=0, receipt_amount=0, calendar_event_id=-1, unique_identifier=-1, date_time_format="ISO"):
        """Initializes the Session.date_time is a string in either ISO or HUMAN(d/m/Y H:M) format"""
        if patient_instance.exists_in_database():
            patient_instance.get_values_from_database_based_on_name()
            self.name = patient_instance.get_name()
            self.patients_id = patient_instance.unique_id
        else:
            self.name = patient_instance.get_name()
        if date_time_format == "HUMAN":
            self.date_time = self.convert_human_datetime_to_iso(date_time)
        elif date_time_format == "ISO":
            self.date_time = date_time
        if price is None:
            self.price = patient_instance.get_price()
        else:
            self.price = price
        self.paid = paid
        self.patient_instance = patient_instance
        self.receipt = receipt
        self.receipt_amount = receipt_amount
        self.calendar_event_id = calendar_event_id
        self.unique_identifier = unique_identifier

    def __str__(self):
        return f"""        Θεραπευόμενος: {self.name}
        Date: {self.date_time}
        Price: {self.price}
        Paid: {self.paid}
        Receipt: {'yes' if self.receipt else 'no'}
        Receipt Amount: {self.receipt_amount}
        Unique_Identifier: {self.unique_identifier}"""

    def has_valid_name(self):
        """Returns True if the patient's name is valid, False otherwise"""

        if len(self.name.split()) < 2 or self.name == "" or any(char in """¨©¬¥«»΅€®²³£§¶¤¦°±½½1234567890!"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.name):
            return False

        return True

    def has_valid_price(self):
        """Returns True if the patient's price field is valid, False otherwise"""
        if self.price == "skata" or any(char in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΌΎΏ¨©¬¥«»΅®²³§¶¤¦°±½½!"#%&\'()*+,-./:;<=>@[\\]^_`{|}~΄""" for char in self.price):
            return False
        elif self.price.strip() == "":
            return False
        return True

    def has_valid_date_time(self):

        try:
            datetime.strptime(
                self.date_time, "%Y-%m-%dT%H:%M:%S%z")

        except (AttributeError, TypeError, ValueError)as er:
            print(er)
            return False

        return True

    @staticmethod
    def write_many_to_database(session_objects):
        """Writes the Sessions's data to the database"""
        conn = None
        print("Entering write_many_to_database")
        try:

            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            # Insert the patient's information into the database
            query = '''INSERT INTO Sessions ("Patient","Datetime","Price","Paid","Patient ID",Receipt,"Receipt Amount") VALUES ( ?, ?, ?, ?, ?,?,?)'''

            values = [(session.name,
                      session.date_time,
                      session.price,
                      session.paid,
                      session.patients_id,
                      session.receipt,
                      session.receipt_amount
                       ) for session in session_objects]

            cursor.executemany(query, values)

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
        finally:
            if conn:
                conn.close()

    def write_yourself_to_database(self):
        """Writes the Sessions's data to the database"""
        if self.patients_id and not self.exists_in_database():
            conn = None
            try:

                conn = sqlite3.connect('REAL_patients - Copy.db')
                cursor = conn.cursor()

                # Insert the patient's information into the database
                query = '''INSERT INTO Sessions ("Patient","Datetime","Price","Paid","Patient ID",Active,Receipt,"Receipt Amount","Calendar Event ID") VALUES ( ?,?, ?, ?, ?, ?,?,?,?)'''

                values = (self.name,
                          self.date_time,
                          self.price,
                          self.paid,
                          self.patients_id,
                          self.patient_instance.active,
                          self.receipt,
                          self.receipt_amount,
                          self.calendar_event_id
                          )

                cursor.execute(query, values)

                # Commit the changes and close the connection
                conn.commit()
                conn.close()
            finally:
                if conn:
                    conn.close()
        else:
            raise ValueError(
                "patient ID not provided or Session already exists in the database")

    def exists_in_database(self):
        """Checks if the Session exists in the database"""
        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            # Search for the Session in the database
            query = '''SELECT * FROM Sessions WHERE patient = ? AND Datetime = ?'''

            values = (self.name, self.date_time)

            cursor.execute(query, values)

            # Check if a matching Session exists
            if cursor.fetchone():
                return True
            else:
                return False
        finally:
            if conn:
                conn.close()

    def set_paid(self, paid_int=None):
        """Sets the paid status of the Session"""
        if paid_int is None:
            raise ValueError("paid_int cannot be None")

        self.paid = paid_int
        self.receipt = 1 if self.paid in range(3, 5) else 0
        self.receipt_amount = self.price if self.receipt else 0
        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()
            # update the Sessions table
            query = '''UPDATE Sessions SET Paid = ?,Receipt=?,"Receipt Amount"=? WHERE "Unique Identifier" = ?'''
            values = (self.paid, self.receipt,
                      self.receipt_amount, self.unique_identifier)
            cursor.execute(query, values)
            conn.commit()
            conn.close()
        finally:
            if conn:
                conn.close()

    def get_values_from_database_based_on_id(self, id_number=-1):
        """Gets the values of the Session from the database based on the id number"""
        if self.unique_identifier == -1 and id_number == -1:
            raise ValueError("id_number cannot be -1")
        elif id_number != -1:
            self.unique_identifier = id_number

        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            query = '''SELECT * FROM Sessions WHERE "Unique Identifier" = ?'''
            values = (self.unique_identifier,)
            cursor.execute(query, values)
            row = cursor.fetchone()
            self.name = row[0]
            self.date_time = row[1]
            self.price = row[2]
            self.paid = row[3]
            self.patients_id = row[4]
            self.unique_identifier = row[6]
            self.receipt = row[7]
            self.receipt_amount = row[8]
            conn.commit()
            conn.close()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def convert_human_datetime_to_iso(date_time):
        """Converts a human readable datetime (ie DD/MM/YYYY HH:MM) to ISO format"""

        date_time_obj = datetime.strptime(date_time, "%d/%m/%Y %H:%M")

        string_datetime = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
        date_time_obj = datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")
        # now we add timezone info
        date_time_obj = pytz.timezone("Europe/Athens").localize(date_time_obj)
        return date_time_obj.isoformat(timespec='seconds')

# ...


# ...

def nearest_weekday(target_weekday, base_datetime):
    # Calculate the number of days to the target weekday
    days_until_target = (target_weekday - base_datetime.weekday() + 7) % 7
    return base_datetime + timedelta(days=days_until_target)


if __name__ == "__main__":
    import random
    from datetime import datetime, timedelta, timezone
    from pytz import timezone
    from patients_management_database import PatientsDatabase

    # Assume 'patients' is your list of Patient objects
    patients = PatientsDatabase.get_patients_as_objects()

    # Define the timezone for Athens, Greece
    athens_tz = pytz.timezone('Europe/Athens')

    # Assign each patient a random day of the week for their sessions
    patient_day_mapping = {patient.get_name(): random.randint(0, 4)
                           for patient in patients}

    # Keep track of the dates already used for each patient
    patient_dates_used = {patient.get_name(): set() for patient in patients}

    sessions = []  # The list to hold your session objects
    for _ in range(10000):
        # Select a random patient
        patient = random.choice(patients)
        patient_name = patient.get_name()
        print(_)
        # Generate a random datetime within a specific range in the past
        # If the date is already used, generate a new one
        # Generate a random datetime within a specific range in the past
        # If the date is already used, generate a new one
        while True:
            random_days_in_past = random.randint(1, 2500)
            naive_datetime = datetime.now() - timedelta(days=random_days_in_past)
            session_day = patient_day_mapping[patient_name]
            naive_datetime = nearest_weekday(session_day, naive_datetime)
            date_string = naive_datetime.strftime('%Y-%m-%d')

            if date_string not in patient_dates_used[patient_name]:
                patient_dates_used[patient_name].add(date_string)
                break

        # Localize the naive datetime object to Athens timezone
        random_datetime = athens_tz.localize(naive_datetime)

        # Generate random hours and minutes
        random_hour = random.randint(8, 21)
        random_minute = random.choice([0, 15, 30, 45])

        # Replace the hour and minute of the datetime with the random values
        random_datetime = random_datetime.replace(
            hour=random_hour, minute=random_minute)

        # Format the datetime as an ISO 8601 string with timezone information
        # strftime is used here instead of isoformat to remove microseconds
        random_datetime_iso = random_datetime.isoformat(timespec='seconds')

        # Create a new session object with the random patient, datetime, and price
        random_paid = random.choices([0, 1, 2, 3, 4], weights=[
                                     4, 66, 10, 10, 10], k=1)[0]
        random_receipt = 1 if random_paid in range(3, 5) else 0
        random_receipt_amount = patient.price if random_receipt else 0

        session = Session(patient_instance=patient, date_time=random_datetime_iso,
                          price=patient.price, paid=random_paid, receipt=random_receipt, receipt_amount=random_receipt_amount, date_time_format="ISO")

        # Add the session to the list
        sessions.append(session)
    Session.write_many_to_database(sessions)
    # for session in sessions:
    #     session.write_yourself_to_database()

    # print(session)
