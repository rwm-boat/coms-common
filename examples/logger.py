from mqtt_client.subscriber import Subscriber
import json
import time

def on_gps_received(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    with open('gps_log.txt', 'a') as outfile:
        json.dump(obj, outfile)
        outfile.write('\n')

def on_compass_received(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    with open('compas_log.txt', 'a') as outfile:
        json.dump(obj, outfile)
        outfile.write('\n')

def on_temp_received(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    with open('temp_log.txt', 'a') as outfile:
        json.dump(obj, outfile)
        outfile.write('\n')

def on_adc_received(client, userdata, message):
    obj = json.loads(message.payload.decode('utf-8'))
    with open('adc_log.txt', 'a') as outfile:
        json.dump(obj, outfile)
        outfile.write('\n')

   
# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    default_subscriptions = {
        # Nav Loggers
        "/status/gps": on_gps_received,
        "/status/compass": on_compass_received,
        # Jet Loggers
        "/status/temp": on_temp_received,
        "/status/adc": on_adc_received
    }
    subber = Subscriber(client_id="logger_client", broker_ip="127.0.0.1", default_subscriptions=default_subscriptions)
    subber.listen()

    while(True):
        # Wait for the broker to retur the message
        time.sleep(.001)


