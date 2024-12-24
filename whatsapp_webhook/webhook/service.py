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
    ACCESS_TOKEN = "EAAHwhtJUljUBO8SpNZBrWhCRIj1Wc3NGYEZAyrZBRkSnotEFsEuNNlSKa8OwbCcba7Jk4NscdAEHj8Jx3PF7ZBR8XBOEVehZBw1hfkcMHOmlf68aOrKocwnzEfDH8T7lvB9rDp5pgBofsrkjqnNa3IQ6ZAQOMtrHHvZCZAU9Yco0O8BkfQB6V2pTznW06uhc3zAr8vrDzPfrh2TBzA0H8IHuob2YZBhwZD"

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
            Message.objects.create(
                                sender="Jaydeep",
                                receiver=recipient,
                                content=text,
                                timestamp=dt_object,
                                status="Sent",
                            )
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