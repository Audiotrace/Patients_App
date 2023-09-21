import sqlite3
from datetime import datetime


from patient import Patient
from session import Session


class PatientsDatabase:
    @staticmethod
    def get_patients_as_list_of_strings(inactive=True):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Name, Age, Telephone, Profession,"Referenced By", Price, "Start Date", Active,ID FROM patients')
        rows = cursor.fetchall()

        conn.close()
        list_of_strings = [[str(e) for e in row]
                           for row in rows if row[7] == 1 or inactive]

        return list_of_strings

    @staticmethod
    def get_patients_as_set_of_tuples(inactive=True) -> set[tuple]:
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Name, Age, Telephone, Profession,"Referenced By", Price, "Start Date", Active,ID FROM patients')
        rows = cursor.fetchall()

        conn.close()
        list_of_tuples = [tuple(row)
                          for row in rows if row[7] == 1 or inactive]
        set_of_tuples = set(list_of_tuples)
        return set_of_tuples

    @staticmethod
    def get_patients_as_objects(inactive=True):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT ID FROM patients')
        ids = cursor.fetchall()

        conn.close()
        list_of_patients = []
        for _id in ids:
            this_patient = Patient(unique_id=_id[0])
            this_patient.get_values_from_database_based_on_id()
            if this_patient.active == 1 or inactive:
                list_of_patients.append(this_patient)

        return list_of_patients


class SessionsDatabase:
    @staticmethod
    def get_sessions_as_list_of_strings(inactive=True):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Datetime,Datetime,Patient, Price, Paid,"Patient ID", Active,"Unique Identifier",Receipt,"Receipt Amount" FROM Sessions')
        rows = cursor.fetchall()

        conn.close()
        list_of_strings = [[str(e) for e in row]
                           for row in rows if row[6] == 1 or inactive]

        for row in list_of_strings:

            row[0] = datetime.strptime(
                row[0], "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
            row[1] = datetime.strptime(
                row[1], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
            if row[1] == "00:00":
                row[1] = "-"

        return list_of_strings

    @staticmethod
    def get_sessions_as_set_of_tuples(inactive=True) -> set[tuple]:
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Datetime,Datetime,Patient, Price, Paid,"Patient ID", Active,"Unique Identifier",Receipt,"Receipt Amount" FROM Sessions')
        rows = cursor.fetchall()

        conn.close()
        list_of_strings = [[str(e) for e in row]
                           for row in rows]

        for row in list_of_strings:

            row[0] = datetime.strptime(
                row[0], "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
            row[1] = datetime.strptime(
                row[1], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
            if row[1] == "00:00":
                row[1] = "-"
        list_of_tuples = [tuple(row)
                          for row in list_of_strings if row[6] == 1 or inactive]
        set_of_tuples = set(list_of_tuples)
        return set_of_tuples

    @staticmethod
    def get_sessions_as_objects(inactive=True):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT Patient, Datetime, Price, Paid,"Patient ID", Active,"Unique Identifier" FROM Sessions')
        rows = cursor.fetchall()

        conn.close()
        list_of_sessions = []
        for row in rows:
            this_patient = Patient(unique_id=row[4])
            this_patient.get_values_from_database_based_on_id()
            this_session = Session(this_patient, unique_identifier=row[6])
            this_session.get_values_from_database_based_on_id(id_number=row[6])
            if this_patient.active == 1 or inactive:
                list_of_sessions.append(this_session)

        return list_of_sessions

    @staticmethod
    def update_session(old_session, new_session):
        success = False
        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            query = '''UPDATE Sessions SET Datetime = ?, Price = ?, Paid = ?,Receipt=?,"Receipt Amount"=? WHERE "Unique Identifier" = ?'''
            values = (new_session.date_time, new_session.price,
                      new_session.paid, new_session.receipt, new_session.receipt_amount, old_session.unique_identifier)
            cursor.execute(query, values)
            conn.commit()
            cursor.execute(
                'SELECT Datetime, Price, Paid FROM Sessions WHERE "Unique Identifier" = ?', (old_session.unique_identifier,))
            row = cursor.fetchone()

            if row[0] == new_session.date_time and row[1] == int(new_session.price) and row[2] == new_session.paid:
                success = True

            return success
        finally:
            conn.close()

    @staticmethod
    def delete_session(session_id):
        success = False
        conn = None
        try:
            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            query = '''DELETE FROM Sessions WHERE "Unique Identifier" = ?'''
            values = (session_id,)
            cursor.execute(query, values)
            conn.commit()
            cursor.execute(
                'SELECT * FROM Sessions WHERE "Unique Identifier" = ?', (session_id,))
            row = cursor.fetchone()

            if row is None:
                success = True

            return success
        finally:
            conn.close()


class GeneralDatabase:

    @staticmethod
    def exists_in_database(calendar_event_id: str) -> bool:

        conn = None
        try:

            conn = sqlite3.connect('REAL_patients - Copy.db')
            cursor = conn.cursor()

            cursor.execute(
                'SELECT * FROM Sessions WHERE "Calendar Event ID" = ?', (calendar_event_id,))
            row = cursor.fetchone()
            conn.close()

            if row is None:
                return False
            else:
                return True
        finally:
            if conn:
                conn.close()

    @staticmethod
    def is_in_ignored_events(event_id: str) -> bool:
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM "Ignored Calendar Events" WHERE ID = ?', (event_id,))
        row = cursor.fetchone()

        conn.close()

        if row is None:
            return False
        else:
            return True

    @staticmethod
    def add_to_ignored_events(calendar_event: list[str]):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO "Ignored Calendar Events" VALUES (?,?,?)', (calendar_event[0]+" "+calendar_event[1], calendar_event[2], calendar_event[4]))
        conn.commit()

        conn.close()

    @staticmethod
    def remove_from_ignored_events(calendar_event_id: str):
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "Ignored Calendar Events" WHERE ID = ?', (calendar_event_id,))
        conn.commit()

        conn.close()

    @staticmethod
    def get_ignored_events() -> list[list[str]]:
        conn = sqlite3.connect('REAL_patients - Copy.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM "Ignored Calendar Events"')
        rows = cursor.fetchall()
        rows = [[str(e) for e in row] for row in rows]
        conn.close()
        return rows
