TOKEN = "your_telegram_bot_token"  # Token from BotFather
PROXIES_URL = "your_proxy_url"     # Optional proxy configurationimport json
import requests
import re
import random
import logging
from requests.exceptions import HTTPError
from configuration_values import PROXIES_URL
import ua_generator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Requester:
    def __init__(self):
        # Generate new UA for each instance and convert to string
        self.ua = str(ua_generator.generate())
        logger.info(f"Generated User-Agent: {self.ua}")

        self.HEADER = {
            "User-Agent": self.ua,
            "Host": "www.vinted.fr",
        }
        self.VINTED_AUTH_URL = "https://www.vinted.fr/"
        self.MAX_RETRIES = 3
        self.session = requests.Session()
        self.session.headers.update(self.HEADER)
        
        # Configure proxy
        self.session.proxies = {
            'http': f'http://{PROXIES_URL}',
            'https': f'http://{PROXIES_URL}'
        }
        logger.info(f"Initialized requester with proxy: {PROXIES_URL}")

    def setLocale(self, locale):
        """
        Set the locale of the requester.
        :param locale: str
        """
        self.VINTED_AUTH_URL = f"https://{locale}/"
        self.HEADER = {
            "User-Agent": self.ua,
            "Host": f"{locale}",
        }
        self.session.headers.update(self.HEADER)
        logger.info(f"Updated locale to: {locale}")

    def get(self, url, params=None):
        """
        Perform a http get request.
        :param url: str
        :param params: dict, optional
        :return: dict
            Json format
        """
        tried = 0
        while tried < self.MAX_RETRIES:
            tried += 1
            logger.info(f"GET request to {url} (attempt {tried}/{self.MAX_RETRIES})")
            with self.session.get(url, params=params) as response:
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 401 and tried < self.MAX_RETRIES:
                    logger.warning(f"Cookies invalid retrying {tried}/{self.MAX_RETRIES}")
                    self.setCookies()
                elif response.status_code == 200 or tried == self.MAX_RETRIES:
                    return response

        logger.error("Max retries reached with no successful response")
        return HTTPError

    def post(self, url, params=None):
        logger.info(f"POST request to {url}")
        response = self.session.post(url, params)
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response

    def setCookies(self):
        logger.info("Clearing session cookies")
        self.session.cookies.clear_session_cookies()

        try:
            self.session.head(self.VINTED_AUTH_URL)
            logger.info("Cookies set successfully!")

        except Exception as e:
            logger.error(f"Error fetching cookies for vinted: {e}")

    # def login(self,username,password=None):

    #     # client.headers["X-Csrf-Token"] = csrf_token
    #     # client.headers["Content-Type"] = "*/*"
    #     # client.headers["Host"] = "www.vinted.fr"
    #     print(self.session.headers)
    #     urlCaptcha = "https://www.vinted.fr/api/v2/captchas"
    #     dataCaptcha = {"entity_type":"login", "payload":{"username": username }}

    #     token_endpoint  = "https://www.vinted.fr/oauth/token"
    #     uuid = self.session.post(urlCaptcha, data=json.dumps(dataCaptcha)).json()["uuid"]
    #     log = {"client_id":"web","scope":"user","username":username,"password":password,"uuid":uuid,"grant_type":"password"}
    #     b = self.session.post(token_endpoint, data=json.dumps(log) )
    #     print(b.text)

    # def message(self):
    #     response = self.session.get("https://www.vinted.fr/api/v2/users/33003526/msg_threads?page=1&per_page=20")
    #     print(response.text)


requester = Requester()
