"""
A program to check available dates for visa appointments.
"""

import logging
from time import sleep
from core.appointment_finder import IDataAppointmentFinder
from core.notifier import WhatsappNotifier

# Configure the logger.
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] -- [%(levelname)s] -- %(name)s (%(funcName)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="idata_available_date_searcher_service.log",
    filemode="a"
)

# Constants
PHONE_NUMBER_1 = "+90xxxxx"
PHONE_NUMBER_2 = "+90xxxxx"

if __name__ == "__main__":
    # Create a logger instance.
    logger = logging.getLogger("iDataAvailableDateSearcher")

    # Add telephone numbers to send Whatsapp messages.
    whatsapp = WhatsappNotifier()
    whatsapp.add_phone_api_key(PHONE_NUMBER_1, "API_KEY")
    whatsapp.add_phone_api_key(PHONE_NUMBER_2, "API_KEY")

    try:
        # Create an appointment finder instance.
        appointments = IDataAppointmentFinder()

        # Add offices to check.
        appointments.add_office("Altunizade", 8)
        appointments.add_office("Gayrettepe", 1)

        while True:
            # Find the next available date.
            for office in ["Altunizade", "Gayrettepe"]:
                free_dates = appointments.find_available_dates(office, search_before="18-11-2023")

                # If there is a next available date, send a Whatsapp message.
                if free_dates:
                    logger.info("[{office}] Next available date: %s", free_dates)
                    message = f"{office} There is a free slot, be fast! {free_dates}"
                    whatsapp.send_message(PHONE_NUMBER_1, message)
                    whatsapp.send_message(PHONE_NUMBER_2, message)

            logger.info("Sleeping for 30 seconds.")
            sleep(60)
    except Exception as e:
        logger.error("An error occured: %s", e)
        whatsapp.send_message(PHONE_NUMBER_1, f"An error occured on iDataAvailableDateSearcher script: {e}")
