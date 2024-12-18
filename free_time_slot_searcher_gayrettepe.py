"""
A program to check available dates for visa appointments.
"""

import logging
from time import sleep
from core.appointment_finder import IDataAppointmentFinder
from core.notifier import WhatsappNotifier
from core.utils import IDataUtilities

# Configure the logger.
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] -- [%(levelname)s] -- %(name)s (%(funcName)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="idata_free_time_searcher_service.log",
    filemode="a"
)

# Constants
TELEPHONE_NO_1 = "+90xxxxxx"
TELEPHONE_NO_2 = "+90xxxxxx"

# Create a logger instance.
logger = logging.getLogger("iDataFreeTimeSlotSearcher-Gayrettepe")


if __name__ == "__main__":
    # Add telephone numbers to send Whatsapp messages.
    whatsapp = WhatsappNotifier()
    whatsapp.add_phone_api_key(TELEPHONE_NO_1, "API_KEY")
    whatsapp.add_phone_api_key(TELEPHONE_NO_2, "API_KEY")

    try:
        # Create an appointment finder instance.
        appointments = IDataAppointmentFinder()
        # Add offices to check.
        appointments.add_office("Gayrettepe", 1)
        logger.info("The program has been initilized.")

        while True:
            # Get the dates between start and end.
            dates_to_check = IDataUtilities.get_dates_between("today", "17-11-2023")

            for date_check in dates_to_check:
                free_time_slots = appointments.check_for_specific_date("Gayrettepe", date_check, "free")

                if free_time_slots:
                    logger.info("[%s] Free time slots: %s", "Gayrettepe", free_time_slots)
                    message = f"There are some free slots in Gayrettepe, be quick: {free_time_slots}"
                    whatsapp.send_message(TELEPHONE_NO_1, message)
                    whatsapp.send_message(TELEPHONE_NO_2, message)

            # Sleep for 30 seconds.
            logger.info("Sleeping for 30 seconds.")
            sleep(30)
    except Exception as e:
        logger.error("An error occured: %s", e)
        whatsapp.send_message(TELEPHONE_NO_1, f"An error occured on Gayrettepe script: {e}")