"""
This module provides functionality to find appointments.
"""

import logging

from core.idata_requester import IDataRequester
from core.utils import IDataUtilities

# Create a logger instance.
logger = logging.getLogger("IDataAppointmentFinder")


class IDataAppointmentFinder:
    """This class functions as a wrapper for requests and provides the 
    functionality of searching and finding free slots.
    """

    def __init__(self):
        # Internal dictionary to store the exit point names and their IDs.
        self._exit_ids: dict[str, int] = {}

        # Set the default values.
        self.consular_id: int = 2
        self.service_type_id: int = 1
        self.calendar_type: int = 2
        self.total_person: int = 1
        self.personal_id: str = \
            "eyJpdiI6ImUzRlYwV0JYbFRFaTdoR2luYkJ4eUE9PSIsInZh" \
            "bHVlIjoicVdUUHpOOWJZclR0OEYxVFJEYkhaZz09IiwibWFj" \
            "IjoiNzY3MGUyNDMxMWUxZDE1ZGQ3MjM4MTU2ODU1MTA1NjAx" \
            "NTA2M2NjOTFlYWQxZGY4YjYwZGIxZjIxMjczN2FhMyJ9"

    def add_office(self, office_name: str, office_id: int) -> None:
        """Add an office name and its ID to check in functions."""
        self._exit_ids[office_name] = office_id

    def find_available_dates(self, office_name: str, search_before: str) -> list[str]:
        """Find the next available date."""
        # Check if the office name is valid.
        if office_name not in self._exit_ids:
            raise ValueError(f"Invalid office name: {office_name}")
        exit_id = self._exit_ids[office_name]

        with IDataRequester() as requester:
            # Get the available dates.
            response: str = requester.post_getdate(
                self.consular_id,
                exit_id, self.service_type_id,
                self.calendar_type,
                self.total_person
            )

            # Parse the available dates.
            available_dates = IDataUtilities.parse_available_dates(response)
            logger.debug("Available dates: %s", available_dates)

            # Check if there are any available dates.
            if not available_dates:
                logger.info("%s: No available dates.", office_name)
                return []

            # Remove dates before the given date.
            dates_before = IDataUtilities.remove_dates_before(
                available_dates,
                allow_before=search_before
            )
            logger.debug("Dates before: %s", dates_before)

            if not dates_before:
                logger.info("%s: No available dates.", office_name)
                return []

            logger.info("[FOUND AVAILABLE DATE] %s: %s", office_name, dates_before)
            return dates_before

    def check_for_specific_date(self,
                                office_name: str,
                                date_to_check: str,
                                time_slot_type: str
                                ) -> list[str]:
        """Check if a specific date is available."""
        # Check if the office name is valid.
        if office_name not in self._exit_ids:
            raise ValueError(f"Invalid office name: {office_name}")
        exit_id = self._exit_ids[office_name]

        with IDataRequester() as requester:
            # Check if the given date is available.
            response: str = requester.post_senddate(
                date_to_check,
                self.total_person,
                self.consular_id,
                exit_id,
                self.calendar_type,
                self.service_type_id,
                self.personal_id
            )

            # Parse the response.
            available_hours = IDataUtilities.parse_available_hours(response, time_slot_type)

            if not available_hours:
                logger.info("%s: No free time slots on %s.", office_name, date_to_check)
                return []

            logger.info("[FOUND TIME SLOT] %s on %s: %s",
                        office_name, date_to_check, available_hours)
            return available_hours
