"""
This module provides functionality to notify the user.
"""

import logging
import requests

# Create a logger instance.
logger = logging.getLogger("WhatsappNotifier")

class WhatsappNotifier:
    """This class provides a Whatsapp notifier."""

    def __init__(self):
        self._phones_api_keys: dict[str, str] = {}
        self._api_url: str = "https://api.callmebot.com/whatsapp.php"

    def add_phone_api_key(self, phone_number: str, api_key: str) -> None:
        """Add a phone number and its API key."""
        self._phones_api_keys[phone_number] = api_key

    def send_message(self, phone_number: str, message: str) -> bool:
        """Send a WhatsApp message to the user."""
        # Get the API key for the given phone number.
        api_key = self._phones_api_keys.get(phone_number, None)
        if not api_key:
            logger.error("No API key found for %s", phone_number)
            exit()

        # Send the request.
        request_url = f"{self._api_url}?phone={phone_number}&text={message}&apikey={api_key}"
        response = requests.get(request_url, timeout=10)

        # Check if the request was unsuccessful.
        if response.status_code != 200:
            logger.error("Failed to send WhatsApp message to %s", phone_number)
            logger.error("Status code: %s", response.status_code)
            return False

        # Log the success.
        logger.info("WhatsApp message (%s) sent to %s", message, phone_number)
        return True
