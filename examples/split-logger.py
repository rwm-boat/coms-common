from mqtt_client.subscriber import Subscriber
import json
import time
from datetime import datetime
from threading import Thread

# Base Name for Log files
_LOG_BASE = "log"


def on_log_received(client, userdata, message):
    global _LOG_BASE
    log_title = message.payload.decode("utf-8")
    time = datetime.today()
    log_time = (
        f"{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}"
    )
    _LOG_BASE = log_title + "_" + log_time
    print(_LOG_BASE)


def on_gps_received(client, userdata, message):
    obj = json.loads(message.payload.decode("utf-8"))
    with open(f"../logs/{_LOG_BASE}_gps.txt", "a") as outfile:
        json.dump(obj, outfile)
        outfile.write("\n")


def on_compass_received(client, userdata, message):
    obj = json.loads(message.payload.decode("utf-8"))
    with open(f"../logs/{_LOG_BASE}_compas.txt", "a") as outfile:
        json.dump(obj, outfile)
        outfile.write("\n")


def on_temp_received(client, userdata, message):
    obj = json.loads(message.payload.decode("utf-8"))
    with open(f"../logs/{_LOG_BASE}_temp.txt", "a") as outfile:
        json.dump(obj, outfile)
        outfile.write("\n")


def on_adc_received(client, userdata, message):
    obj = json.loads(message.payload.decode("utf-8"))
    with open(f"../logs/{_LOG_BASE}_adc.txt", "a") as outfile:
        json.dump(obj, outfile)
        outfile.write("\n")


# ==================
# -- MAIN METHOD --
# ==================
if __name__ == "__main__":

    default_subscriptions = {
        # Nav Loggers
        "/status/gps": on_gps_received,
        "/status/compass": on_compass_received,
        # Jet Loggers
        "/status/temp": on_temp_received,
        "/status/adc": on_adc_received,
        # Commands
        "/command/logging": on_log_received,
    }
    subber = Subscriber(
        client_id="logger_client",
        broker_ip="192.168.8.170",
        default_subscriptions=default_subscriptions,
    )

    # Start a thread to run the callback functions for you
    # You need this if you're doing anything after the subber.listen() call
    thread = Thread(target=subber.listen)
    thread.start()
