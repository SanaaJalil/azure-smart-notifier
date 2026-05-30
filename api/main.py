from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import logging
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICEBUS_CONNECTION_STRING = os.getenv("SERVICEBUS_CONNECTION_STRING")
SERVICEBUS_QUEUE_NAME = os.getenv("SERVICEBUS_QUEUE_NAME", "notifications")

app = FastAPI(
    title="Azure Smart Notifier",
    description="Accepts messages and routes them through Azure Service Bus",
    version="1.0.0"
)


class NotificationRequest(BaseModel):
    message: str
    recipient: str
    priority: str = "normal"

    class Config:
        orm_mode = True


class NotificationResponse(BaseModel):
    status: str
    message: str
    recipient: str

    class Config:
        orm_mode = True


def send_to_service_bus(payload: dict):
    try:
        client = ServiceBusClient.from_connection_string(SERVICEBUS_CONNECTION_STRING)
        with client:
            sender = client.get_queue_sender(queue_name=SERVICEBUS_QUEUE_NAME)
            with sender:
                message = ServiceBusMessage(json.dumps(payload))
                sender.send_messages(message)
                logger.info(f"Message sent to Service Bus queue: {SERVICEBUS_QUEUE_NAME}")
    except Exception as e:
        logger.error(f"Failed to send message to Service Bus: {e}")
        raise


@app.get("/")
def root():
    return {"status": "Azure Smart Notifier is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/notify", response_model=NotificationResponse)
def send_notification(request: NotificationRequest):
    logger.info(f"Received notification for {request.recipient}: {request.message}")

    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if not request.recipient:
        raise HTTPException(status_code=400, detail="Recipient cannot be empty")

    payload = {
        "message": request.message,
        "recipient": request.recipient,
        "priority": request.priority
    }

    send_to_service_bus(payload)

    return NotificationResponse(
        status="queued",
        message=request.message,
        recipient=request.recipient
    )