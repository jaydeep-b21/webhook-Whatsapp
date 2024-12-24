import requests
import logging
from webhook.models import Message

# Configure logging to log to a file and console
logger = logging.getLogger(__name__)

# Set up log file handler and formatter
file_handler = logging.FileHandler('app.log')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

class WhatsAppService:
    BASE_URL = "https://graph.facebook.com/v21.0/552952211226957/messages"
    ACCESS_TOKEN = "EAAHwhtJUljUBO6U3cEKqqxMxoWOcgHfmjZC1VuODD9J2dZBmnzUR9Jvq5hVOSrZCeSCjpFotzDQkyahnqS1P0fhm7NhB1bEF4QSg8TnxhvRPBZBgbU4appMv7f39diZBICvFlTtpgD2OP8A2jYuvVj1ZAGqSFNM1EObih9YMTuYA9AYPqaxTEcSBmjm5gcpa7xRShM2NDv7zhz3UD1O9Xm3hNyReof"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    def send_message(self, mobile_no, message):
        """
        Sends a message via the WhatsApp Business API.
        :param mobile_no: Recipient's phone number
        :param message: Message content
        :return: Tuple (success: bool, response: dict)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": mobile_no,
            "text": {"body": message},
        }

        try:
            logger.info(f"Sending message to {mobile_no}: {message}")
            response = requests.post(self.BASE_URL, json=payload, headers=self.headers)

            if response.status_code == 200:
                logger.info(f"Message successfully sent to {mobile_no}")
                return True, response.json()
            else:
                logger.error(f"Failed to send message: {response.text}")
                return False, response.json()

        except Exception as e:
            logger.exception("An error occurred while sending the message.")
            return False, {"error": str(e)}
        
        
    def send_message_auto(self, recipient, text, dt_object):
        """
        Sends a message via the WhatsApp Business API and saves it to the database.
        
        :param recipient: Recipient's phone number
        :param text: Message content
        :param dt_object: Timestamp of the message
        :return: Tuple (success: bool, response: dict)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "text": {"body": f"Received your message: {text} with this time {dt_object}"},
        }

        try:
            # Save the message to the database
            message = Message(
                sender="Jaydeep",
                receiver=recipient,
                content=text,
                timestamp=dt_object,
                mobile_no=recipient,
            )
            message.save()
            logger.info(f"Message saved to database for recipient {recipient}")

            # Send the message
            response = requests.post(self.BASE_URL, json=payload, headers=self.headers)

            if response.status_code == 200:
                logger.info(f"Message successfully sent to {recipient}")
                return True, response.json()
            else:
                logger.error(
                    f"Failed to send message to {recipient}: {response.text}"
                )
                return False, response.json()

        except Exception as e:
            logger.exception("An error occurred while sending the message.")
            return False, {"error": str(e)}