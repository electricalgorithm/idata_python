"""
This module is a requester for iDATA website.
"""
import logging

from bs4 import BeautifulSoup
import requests



# Create a logger instance.
logger = logging.getLogger("IDataRequester")


class IDataRequester:
    """This class encapsulates all the requests to the iDATA website."""
    URL_APPOINTMENT_FORM = "https://deu-schengen.idata.com.tr/tr/appointment-form"
    URL_GET_CALENDER_STATUS = "https://deu-schengen.idata.com.tr/tr/getcalendarstatus"
    URL_PASSPORT_CONTROL = "https://deu-schengen.idata.com.tr/tr/personal/passport-control"
    URL_GET_DATE = "https://deu-schengen.idata.com.tr/tr/getdate"
    URL_SEND_DATE = "https://deu-schengen.idata.com.tr/tr/senddate"

    def __init__(self):
        self.session = requests.Session()
        self._xsrf_token, self._x_csrf_token = self.receive_tokens()

    def __del__(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def receive_tokens(self) -> tuple[str, str]:
        """Send a GET request to the homepage."""
        response = self.session.get(self.URL_APPOINTMENT_FORM, timeout=10)

        # Check if the request was successful.
        if response.status_code != 200:
            logger.error("GET request to homepage failed.")
            logger.error("Status code: %s", response.status_code)
            exit()
        logger.debug("GET request to homepage successful.")

        # Extract the XSRF-TOKEN cookie.
        _xsrf_token = self.session.cookies.get('XSRF-TOKEN')
        logger.debug("XSRF-TOKEN: %s", _xsrf_token)

        # Find the X-CSRF-TOKEN from the HTML.
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})

        # Check if the X-CSRF-TOKEN was found.
        if not csrf_meta:
            logger.error("Failed to find X-CSRF-TOKEN in HTML.")
            logger.error("Status code: %s", response.status_code)
            exit()

        # Extract the X-CSRF-TOKEN.
        _x_csrf_token = csrf_meta['content']
        logger.debug("X-CSRF-TOKEN: %s", _x_csrf_token)

        # Set the cookies.
        self.session.cookies.set('c_policy', 'ok')
        self.session.cookies.set('visited', 'yes')
        logger.debug("Cookies set: %s", self.session.cookies)

        return _xsrf_token, _x_csrf_token

    def get_headers(self) -> dict[str, str]:
        """Returns headers needed for requests."""
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0)",
            "Accept": "*/*",
            "Accept-Language": "tr,en-US;q=0.7,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRF-TOKEN": self._x_csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    def post_request(self, url: str, data: dict) -> requests.Response:
        """Sends a POST request to the given address."""
        response = self.session.post(url, headers=self.get_headers(), data=data, timeout=10)
        logger.debug("Response status code: %s", response.status_code)
        return response

    def post_getcalenderstatus(self,
                               visa_office_id: int,
                               service_type_id: int,
                               visa_country_id: int
                               ) -> str:
        """Sends the request to get the calendar status."""
        data = {
            "getvisaofficeid": str(visa_office_id),
            "getservicetypeid": str(service_type_id),
            "getvisacountryid": str(visa_country_id)
        }
        response = self.post_request(self.URL_GET_CALENDER_STATUS, data)
        return response.text

    def post_passaport_control(self,
                               passport: str,
                               country_id: int
                               ) -> str:
        """Sends the request to get the passport control."""
        data = {
            "passport[]": passport,
            "country_id": str(country_id),
        }
        response = self.post_request(self.URL_PASSPORT_CONTROL, data)
        return response.text

    def post_getdate(self,
                     consular_id: int,
                     exit_id: int,
                     service_type_id: int,
                     calendar_type: int,
                     total_person: int
                     ) -> str:
        """Send a POST request to get the available dates."""
        data = {
            'consularid': str(consular_id),
            'exitid': str(exit_id),
            'servicetypeid': str(service_type_id),
            'calendarType': str(calendar_type),
            'totalperson': str(total_person),
        }
        response = self.post_request(self.URL_GET_DATE, data)
        return response.text

    def post_senddate(self,
                      full_date: str,
                      total_person: int,
                      set_new_consular_id: int,
                      set_new_exit_office_id: int,
                      calendar_type: int,
                      set_new_service_type_id: int,
                      personal_info: str
                      ) -> str:
        """Send a POST request to check if selected date is free."""
        data = {
            'fulldate': full_date,
            'totalperson': str(total_person),
            "set_new_consular_id": str(set_new_consular_id),
            "set_new_exit_office_id": str(set_new_exit_office_id),
            "calendarType": str(calendar_type),
            "set_new_service_type_id": str(set_new_service_type_id),
            "personalinfo": personal_info
        }
        response = self.post_request(self.URL_SEND_DATE, data)
        return response.text
