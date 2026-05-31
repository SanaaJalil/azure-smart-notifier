import azure.functions as func
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = func.FunctionApp()

@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="notifications",
    connection="SERVICEBUS_CONNECTION_STRING"
)
def process_notification(msg: func.ServiceBusMessage):
    logging.info("Azure Function triggered by Service Bus message")

    try:
        message_body = msg.get_body().decode("utf-8")
        payload = json.loads(message_body)

        recipient = payload.get("recipient", "unknown")
        message = payload.get("message", "")
        priority = payload.get("priority", "normal")

        logging.info(f"Processing notification:")
        logging.info(f"  Recipient : {recipient}")
        logging.info(f"  Message   : {message}")
        logging.info(f"  Priority  : {priority}")

        if priority == "high":
            logging.warning(f"HIGH PRIORITY alert for {recipient}: {message}")
        else:
            logging.info(f"Notification processed for {recipient}")

        logging.info("Message processed successfully")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise