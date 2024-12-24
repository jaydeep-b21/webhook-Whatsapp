import logging
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime
from django.shortcuts import render
from webhook.models import Message
from rest_framework.decorators import api_view
from webhook.service import WhatsAppService

# This is the token you set up in your Meta Developer Console
VERIFY_TOKEN = "verify_token"  # Replace with your actual token

# Enable logging to inspect incoming requests
# Configure logging to log to a file and console
logger = logging.getLogger(__name__)

# Set up log file handler and formatter
file_handler = logging.FileHandler('incomingrequest_app.log')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

@csrf_exempt
def webhook(request):
    """
    Handles GET requests for webhook verification and POST requests for processing incoming WhatsApp messages.
    """
    if request.method == 'GET':
        token_sent = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        # Log the token and challenge values
        logger.info(f"Token Sent: {token_sent}, Challenge: {challenge}")

        if token_sent == VERIFY_TOKEN:
            logger.info("Webhook verified successfully.")
            return HttpResponse(challenge)  # Send challenge value back to Meta
        else:
            logger.error("Token mismatch or missing.")
            return HttpResponse("Verification failed", status=403)

    elif request.method == 'POST':
        # Handle incoming messages
        try:
            data = json.loads(request.body.decode('utf-8'))
            logger.info(f"Received message data: {json.dumps(data, indent=2)}")

            # Process the entries in the received data
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    messages = change['value'].get('messages', [])
                    for msg in messages:
                        sender = msg.get('from')  # Sender's phone number
                        message_body = msg.get('text', {}).get('body')  # Message content
                        timestamp = msg.get('timestamp')  # Message timestamp (UNIX)
                        dt_object = datetime.utcfromtimestamp(int(timestamp))  # Convert to datetime

                        # Log the incoming message details
                        logger.info(f"Received message from {sender}: {message_body} at {dt_object}")

                        # Respond to the message
                        Message.objects.create(
                                sender="Jaydeep",
                                receiver=sender,
                                content=message_body,
                                timestamp=dt_object,
                                mobile_no=sender,
                                status="Received"
                            )
            return JsonResponse({"status": "success"})

        except Exception as e:
            logger.exception("Error processing incoming message.")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    else:
        return HttpResponse("Invalid request method", status=405)



@api_view(["POST"])
def reply_to_user(request):
    """
    View to handle user replies and send WhatsApp messages via the service layer.
    """
    mobile_no = request.data.get("mobile")
    msg = request.data.get("msg")

    # Validate input
    if not mobile_no or not msg:
        return JsonResponse(
            {"status": "error", "message": "Mobile number and message are required."},
            status=400,
        )

    # Instantiate the WhatsAppService
    whatsapp_service = WhatsAppService()
    success, response = whatsapp_service.send_message(mobile_no, msg)

    if success:
        return JsonResponse(
            {"status": "success", "message": "Message sent successfully."}, status=200
        )
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": "Failed to send message.",
                "details": response,
            },
            status=500,
        )


def admin_interface(request):
    messages = Message.objects.all()
    msg=[]
    # Iterate through the queryset and print the data
    for message in messages:
        msg1={}
        msg1["sender"]=message.sender
        msg1["receiver"]=message.receiver
        msg1["content"]=message.content
        msg1["timestamp"]=message.timestamp
        msg1["status"]=True
        msg1["mobile_no"]=message.mobile_no
        msg.append(msg1)
    # print("Rendering admin interface with messages:", messages)
    return render(request, "admin_interface.html", {"messages": msg})

