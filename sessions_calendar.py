"""This module contains the LessonCalendar class"""

import os.path
from datetime import datetime, timedelta
import pickle
from pytz import timezone
from greek_language import GreekLanguage
from itertools import cycle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class SessionsCalendar:
    """A class to represent the lessons calendar."""

    def __init__(self, calendar_name="spirenabest@gmail.com"):

        self.calendar_name = calendar_name
        self.credentials = self.get_credentials()
        self.calendar_id = self.get_calendar_id()
        self.websites = [
            "http://www.google.com",
            "http://www.amazon.com",
            "http://www.reddit.com",
            "http://www.wikipedia.org",
            "http://www.microsoft.com",
            "http://www.yahoo.com",
            "http://www.bing.com",
            "http://www.linkedin.com",
            "http://www.twitter.com",
            "http://www.facebook.com"
        ]
        self.websites_iter = cycle(self.websites)

    def is_connected(self):
        """Check internet connection by sending a request to a list of websites cyclically."""
        timeout = 5
        failed_attempts = 0
        while failed_attempts < 2:
            try:
                url = next(self.websites_iter)
                _ = requests.get(url, timeout=timeout)
                return True
            except requests.ConnectionError:
                print(f"Failed to connect to {url}, trying next one.")
                failed_attempts += 1
        print("Failed to connect twice, connection might be down.")
        return False

    def get_credentials(self):
        """Gets valid user credentials from storage."""
        creds = None
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading credentials from token.pickle: {e}")
            return None

        try:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secret_734526120322-7ihtv9h3l3va905cecjlu1heoreeq2c3.apps.googleusercontent.com.json', SCOPES)
                    creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
        except Exception as e:
            print(f"Error getting or refreshing credentials: {e}")
            return None

        return creds

    def get_calendar_id(self):
        """Gets the calendar id from the calendar name."""
        try:
            # pylint: disable=no-member
            service = build('calendar', 'v3', credentials=self.credentials)
            calendar_list = service.calendarList().list().execute()

            for calendar_entry in calendar_list['items']:
                if calendar_entry['summary'] == self.calendar_name:
                    return calendar_entry['id']
        except Exception as e:
            print(f"Error getting calendar ID: {e}")

        return None

    def format_date(self, datetime_object, time=False):
        """Returns a datetime object in the format 'dd/mm/yyyy'
        If time is True it will print the time as well
        """

        if time:
            return datetime_object.strftime("%d/%m/%Y %H:%M")
        else:
            return datetime_object.date().strftime("%d/%m/%Y")

    def get_events(self, start_date: str, end_date=None) -> list[tuple]:
        """Gets the past events from the calendar from 00:00:00 of start date
        until 23:59:59 of end date.
        If end date is not specified it will be set
        to start date.
        If end date is set to "now" it will be set to the current
        date and time.
        Returns a list of Tuples
        (date(datetime.datetime),description(str),event_id(str))
        input date format is '%d/%m/%Y'"""

        input_date_format = "%d/%m/%Y %H:%M:%S"
        if end_date is None:
            end_date = start_date+" 23:59:59"
            end_date_obj = datetime.strptime(end_date, input_date_format).astimezone(
                timezone('Europe/Athens'))
        elif end_date.upper() == "NOW":
            end_date_obj = datetime.now().astimezone(
                timezone('Europe/Athens')).replace(microsecond=0)

        else:
            end_date += " 23:59:59"
            end_date_obj = datetime.strptime(
                end_date, input_date_format).astimezone(
                timezone('Europe/Athens'))
        start_date += " 00:00:00"

        start_date_obj = datetime.strptime(
            start_date, input_date_format).astimezone(
            timezone('Europe/Athens'))

        start_date_str = start_date_obj.isoformat()

        end_date_str = end_date_obj.isoformat()

        service = build('calendar', 'v3', credentials=self.credentials)
        self.format_date(start_date_obj.time(), time=True)
        if self.calendar_id is None:
            print(
                f"Could not find calendar with the name '{self.calendar_name}'.")

            return
        # pylint: disable=no-member
        events_result = service.events().list(
            calendarId=self.calendar_id,
            timeMax=end_date_str,
            timeMin=start_date_str,
            singleEvents=True,
            orderBy='startTime',
            maxResults=2000
        ).execute()

        events_from_google = events_result.get('items', [])

        if not events_from_google:
            print(
                f"No events found in the '{self.calendar_name}' calendar.")
            return
        output = []

        for this_event in events_from_google:
            summary = this_event['summary']
            if '"' in summary or '“' in summary or '”' in summary:

                continue

            start = this_event['start'].get(
                'dateTime', this_event['start'].get('date'))
            start_datetime = datetime.strptime(
                start, "%Y-%m-%dT%H:%M:%S%z")
            start_datetime = start_datetime.isoformat()

            output.append((start_datetime, summary, this_event['id']))

        return output

    # def create_event(self, summary, start_date_time, end_date_time, recurrence=None, description=None, reminders=None):
    #     """Creates a new event in the calendar."""

    #     new_event = {
    #         'summary': summary,
    #         'start': {
    #             'dateTime': start_date_time.isoformat(),
    #             'timeZone': 'Europe/Athens',
    #         },
    #         'end': {
    #             'dateTime': end_date_time.isoformat(),
    #             'timeZone': 'Europe/Athens',
    #         },
    #     }

    #     if description:
    #         new_event['description'] = description

    #     if recurrence:
    #         new_event['recurrence'] = recurrence

    #     if reminders:
    #         new_event['reminders'] = reminders

    #     service = build('calendar', 'v3', credentials=self.credentials)
    #     # pylint: disable=no-member
    #     created_event = service.events().insert(
    #         calendarId=self.calendar_id, body=new_event).execute()
    #     print(f"Event created: {created_event.get('htmlLink')}")
    #     return created_event

    # def update_event(self, event_id, summary=None, start_date_time=None, end_date_time=None, recurrence=None, description=None, reminders=None):
    #     """Updates an existing event in the calendar."""

    #     updated_event = {}

    #     if summary:
    #         updated_event['summary'] = summary

    #     if start_date_time:
    #         updated_event['start'] = {
    #             'dateTime': start_date_time.isoformat(),
    #             'timeZone': 'Europe/Athens',
    #         }

    #     if end_date_time:
    #         updated_event['end'] = {
    #             'dateTime': end_date_time.isoformat(),
    #             'timeZone': 'Europe/Athens',
    #         }

    #     if description:
    #         updated_event['description'] = description

    #     if recurrence:
    #         updated_event['recurrence'] = recurrence

    #     if reminders:
    #         updated_event['reminders'] = reminders

    #     service = build('calendar', 'v3', credentials=self.credentials)
    #     # pylint: disable=no-member
    #     updated = service.events().patch(
    #         calendarId=self.calendar_id, eventId=event_id, body=updated_event).execute()
    #     print(f"Event updated: {updated.get('htmlLink')}")
    #     return updated

    # def delete_event_by_details(self, target_summary, target_start_date, target_start_time):
    #     """Deletes an event based on the summary(Title), start date, and start time.
    #     Start date and time should be in the format 'dd/mm/yyyy' and 'HH:MM' respectively.
    #     Returns True if the event was deleted successfully, False otherwise."""

    #     target_date_obj = datetime.strptime(
    #         target_start_date, "%d/%m/%Y").date()
    #     target_time_obj = datetime.strptime(target_start_time, "%H:%M").time()

    #     same_day_events = self.get_events(target_start_date, target_start_date)
    #     if same_day_events is None:
    #         return False
    #     for event_datetime, summary, event_id in same_day_events:
    #         event_date = datetime.strptime(
    #             event_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
    #         event_start_time = datetime.strptime(
    #             event_datetime, "%Y-%m-%dT%H:%M:%S%z").time()

    #         if target_date_obj == event_date and target_time_obj == event_start_time and target_summary == summary:
    #             if self.delete_event(event_id):
    #                 return True
    #             else:
    #                 return False

    #     print(
    #         f"No event found with date {target_start_date}, start time {target_start_time}, and summary '{target_summary}'.")
    #     return False

    # def delete_event(self, event_id):
    #     """Deletes a specific event in the calendar based on the event ID."""

    #     service = build('calendar', 'v3', credentials=self.credentials)
    #     try:
    #         # pylint: disable=no-member
    #         service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
    #         print(f"Event with ID {event_id} has been deleted.")
    #     except HttpError as error:
    #         print(f"An error occurred: {error}")
    #         return False
    #     return True
    def write_to_valid_events_file(self, text):
        # Specify the file to write to
        filename = "valid.txt"

        # Open the file in append mode with explicit UTF-8 encoding
        with open(filename, "a", encoding="utf-8") as file:
            # Write the text to the file and add a newline at the end
            file.write(text + '\n')

    def write_to_invalid_events_file(self, text):
        # Specify the file to write to
        filename = "invalid.txt"

        # Open the file in append mode with explicit UTF-8 encoding
        with open(filename, "a", encoding="utf-8") as file:
            # Write the text to the file and add a newline at the end
            file.write(text + '\n')

    def filter_events(self, events: list[tuple]) -> list[tuple]:
        """Filters the events that are not related to sessions."""
        if events is None:
            return None
        # We need to remove the events that contain special characters because these events are not related to sessions
        illegal_characters = ['"',  '“', '”']

        filtered_events = []
        invalid_index = 0
        valid_index = 0
        invalid_idxs = []
        for idx, event in enumerate(events):
            if any(char in event[1] for char in illegal_characters):
                invalid_index += 1
                invalid_idxs.append(idx)
                continue

            split_event = event[1].strip().split()
            filtered_events.append(
                (event[0], " ".join(split_event), event[2]))
            valid_index += 1

        # print(f"Valid events: {valid_index}")
        # print(f"Invalid events: {invalid_index}")

        self._log_output(events, filtered_events,
                         invalid_index, valid_index, invalid_idxs)
        return filtered_events

    def _log_output(self, events, filtered_events, invalid_index, valid_index, invalid_idxs):
        """Logs the output of filtering method to two files.
        Valid events are logged to valid.txt and invalid events are logged to invalid.txt"""
        self.write_to_valid_events_file(
            f"Start of valid events. Total: {valid_index}.Date is now: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        for event in filtered_events:
            self.write_to_valid_events_file(f"{event[0]} {event[1]}")

        self.write_to_valid_events_file(
            f"End of valid events. Total: {valid_index}.Date is now: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.write_to_valid_events_file("\n")

        self.write_to_invalid_events_file(
            f"Start of invalid events. Total: {invalid_index}.Date is now: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        for idx in invalid_idxs:
            self.write_to_invalid_events_file(
                f"{events[idx][0]} {events[idx][1]}")
        self.write_to_invalid_events_file(
            f"End of invalid events. Total: {invalid_index}.Date is now: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.write_to_invalid_events_file("\n")


if __name__ == "__main__":
    calendar = SessionsCalendar()
    unique_names = []
    events = calendar.get_events("01/01/2023", "now")
    filtered_events = calendar.filter_events(events)
