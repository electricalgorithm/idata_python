"""
This module collects all the utility functions.
"""
import logging
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup

# Create a logger instance.
logger = logging.getLogger("IDataUtilities")

class IDataUtilities:
    """This class encapsulates all the utility functions."""

    @staticmethod
    def parse_available_dates(html_code: str) -> list[str]:
        """Parses the HTML response and returns a list of available dates."""
        # Parse the HTML code
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find all elements with the "form-control" class
        form_control_elements = soup.find_all(class_='form-control')

        # Extract the text from these elements and store them in a list
        result = [element.get_text(strip=True) for element in form_control_elements]
        logger.debug("Available dates parsed: %s", result)
        return result

    @staticmethod
    def remove_dates_before(dates: list[str], allow_before: str) -> list[str]:
        """Remove dates before the given date."""
        allow_before_date = datetime.strptime(allow_before, "%d-%m-%Y").date()
        return [
            date
            for date in dates
            if datetime.strptime(date, "%d-%m-%Y").date() < allow_before_date
        ]

    @staticmethod
    def parse_available_hours(html_code: str, time_slot_type: str) -> list[str]:
        """Parses the HTML response and returns a list of available hours."""
        # Parse the HTML code
        soup = BeautifulSoup(html_code, 'html.parser')

        if time_slot_type == "free":
            # Find all button elements with getdatebtn and noPrime classes.
            button_elements = soup.find_all(class_='noPrime')
        elif time_slot_type == "prime":
            # Find all button elements with getdatebtn and yesPrime classes.
            button_elements = soup.find_all(class_='yesPrime')
        elif time_slot_type == "vip":
            # Find all button elements with getdatebtn and yesVip classes.
            button_elements = soup.find_all(class_="yesVip")
        else:
            # Find all button elements with getdatebtn.
            button_elements = soup.find_all(class_='getdatebtnhour')

        # Extract the text from these elements and store them in a list
        result = [element.get_text(strip=True) for element in button_elements]
        logger.debug("Available hours parsed: %s", result)
        return result

    @staticmethod
    def get_dates_between(from_date: str, until_date: str) -> list[str]:
        """Returns a list of dates in string "dd-mm-yyyy" format 
        from the date today and until the date 18-11-2023.
        """
        if from_date == "today":
            start_date = date.today()
        else:
            # Split the string to day, month and year.
            day, month, year = from_date.split("-")
            start_date = date(int(year), int(month), int(day))

        # Split the until_date given into date object.
        day, month, year = until_date.split("-")
        end_date = date(int(year), int(month), int(day))

        # Find the time difference between start and end time.
        time_difference = end_date - start_date

        # Construct the dates.
        dates = [start_date + timedelta(days=i) for i in range(time_difference.days + 1)]
        return [date.strftime("%d-%m-%Y") for date in dates]
