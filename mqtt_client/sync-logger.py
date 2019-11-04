import sys,os
import curses
import time
from mqtt_client.subscriber import Subscriber
from mqtt_client.publisher import Publisher
from threading import Thread
import json
from datetime import datetime

# global variables for logging
mag_compass_reading = 0
int_compass_reading = 0
time_reading = 0
lat_reading = 0
lon_reading = 0
speed_reading = 0
gps_heading_reading = 0
jet1_temp = 0
jet2_temp = 0
compartment_temp = 0
gps_distance = 0
jet1_current = 0 #starboard
jet2_current = 0 #port
pack_voltage = 0

prev_name = None
cur_name = None

# Base Name for Log files
_LOG_BASE = "log"

pubber = Publisher(client_id="logger-pubber")

def on_log_received(client, userdata, message):
    global _LOG_BASE
    log_title = message.payload.decode("utf-8")
    time = datetime.today()
    log_time = (
        f"{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}"
    )
    _LOG_BASE = log_title + "_" + log_time
    print("received")
    
def on_temp_received(client, userdata, message):
    global jet1_temp
    global jet2_temp
    global compartment_temp

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_temp = obj["jet1_temp"]
    jet2_temp = obj["jet2_temp"]
    compartment_temp = obj["compartment_temp"]

def on_compass_received(client, userdata, message):
    global mag_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    mag_compass_reading = obj['compass']

def on_internal_compass_received(client, userdata, message):
    global int_compass_reading
    obj = json.loads(message.payload.decode('utf-8'))
    int_compass_reading = obj['heading']

def on_gps_received(client, userdata, message):
    # create global variables for UI
    global time_reading
    global lat_reading
    global lon_reading
    global speed_reading
    global gps_heading_reading
    global gps_distance
    
    obj = json.loads(message.payload.decode('utf-8'))

    # parse json into global variablesspeed_reading,
    time_reading = obj["time"]
    lat_reading = obj['latitude']
    lon_reading = obj['longitude']
    speed_reading = obj["speed"]
    gps_heading_reading = obj["course"]
    gps_distance = obj['distance']

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current
    global pack_voltage

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = obj["jet1_amps"]
    jet2_current = obj["jet2_amps"]
    pack_voltage = obj["pack_voltage"]

# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':


    try:
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/internal_compass" : on_internal_compass_received,
            "/status/temp" : on_temp_received,
            "/command/logging" : on_log_received
            
        }
        subber = Subscriber(client_id="telemetry_live", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()
        print("here")

        while True:
            message = {
                'time' : time_reading,
                'speed' : speed_reading,
                'jet1_current' : jet1_current,
                'jet2_current' : jet2_current,
                'mag_compass' : mag_compass_reading,
                'int_compass' : int_compass_reading,
                'gps_heading' :gps_heading_reading,
                'latitude' : lat_reading,
                'longitude' : lon_reading,
                'distance' : gps_distance,
                'jet1_temp' : jet1_temp,
                'jet2_temp' : jet2_temp,
                'compartment_temp' : compartment_temp,
                'pack_voltage' : pack_voltage
            }
            with open(f"../logs/{_LOG_BASE}.txt", "a") as outfile:
                json.dump(message, outfile)
                outfile.write("\n")
                    
            time.sleep(0.1)

            cur_name = _LOG_BASE

            name_message = {
            
                'name' : _LOG_BASE

            }
            if(cur_name is not prev_name):
                app_json = json.dumps(name_message)
                pubber.publish("/status/log_name",app_json)
                print(name_message)

            prev_name = cur_name

    except KeyboardInterrupt:
        
        print("-End Logger-")
       