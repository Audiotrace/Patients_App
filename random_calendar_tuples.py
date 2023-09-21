import datetime
import random
import pytz
import names


class RandomCalendarEvents:
    def __init__(self):
        self.data = self.generate_random_data()

    def random_date(self, start, end):
        """Generate a random datetime between `start` and `end`"""
        return start + datetime.timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())))

    def format_iso_with_colon(self, dt):
        """Formats the datetime in ISO 8601 format with a colon in the timezone offset"""
        tz_string = dt.strftime('%z')
        return dt.strftime('%Y-%m-%dT%H:%M:%S') + tz_string[:-2] + ":" + tz_string[-2:]

    def generate_random_data(self):
        # Define an empty list to store the tuples
        data = []

        # Define a set to store the IDs that have already been generated
        used_ids = set()

        # Define the timezone for Athens, Greece
        athens_tz = pytz.timezone('Europe/Athens')

        # Define start and end dates for random date generation (in Athens timezone)
        start_date = datetime.datetime(
            2000, 1, 1, tzinfo=pytz.utc).astimezone(athens_tz)
        end_date = datetime.datetime(
            2023, 6, 16, tzinfo=pytz.utc).astimezone(athens_tz)

        # Loop 1000 times to generate 1000 tuples
        for _ in range(200):
            # Generate random datetime (in Athens timezone)
            random_dt = self.random_date(start_date, end_date)
            # Format the datetime string in ISO 8601 format with a colon in the timezone offset
            timestamp = self.format_iso_with_colon(random_dt)

            # Generate random name and surname
            name = names.get_full_name()

            # Generate a unique random integer ID
            while True:
                random_id = random.randint(1, 1000000)
                if random_id not in used_ids:
                    used_ids.add(random_id)
                    break

            # Append the tuple (timestamp, name, random_id) to the list
            data.append((timestamp, name, random_id))

        # Return the generated list of tuples
        return data


if __name__ == '__main__':
    # Printing first 10 entries to show the format
    random_calendar_events = RandomCalendarEvents()
    print(random_calendar_events.data)
