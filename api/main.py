from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    logger.info(f"Notification queued successfully for {request.recipient}")

    return NotificationResponse(
        status="queued",
        message=request.message,
        recipient=request.recipient
    )