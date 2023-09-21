import sqlite3
import random
from patients_management_database import PatientsDatabase

# Connect to the database
conn = sqlite3.connect('REAL_patients - Copy.db')
cursor = conn.cursor()
patients = PatientsDatabase.get_patients_as_objects()
# Get the total number of rows in the table
total_patients = len(patients)
print(f"Total rows: {total_patients}")

# Calculate the number of rows to set as active (75%)
active_patients = int(0.85 * total_patients)
print(f"Active patients: {active_patients}")
# Create a list of indices to set as active
active_ids = random.sample(
    [patient.unique_id for patient in patients], active_patients)
print(f"Active ids: {active_ids}")
# Update the Active column for each row

for patient in patients:
    active = 1 if patient.unique_id in active_ids else 0
    cursor.execute("UPDATE patients SET Active = ? WHERE ID = ?",
                   (active, patient.unique_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
