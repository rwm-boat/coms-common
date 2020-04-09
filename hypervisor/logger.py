import sys
import os
import json
from datetime import datetime
from threading import Thread
from mqtt_client.subscriber import Subscriber
from mqtt_client.publisher import Publisher

curr_state = {
    'mag_compass_reading': 0,
    'int_compass_reading': 0,
    'time_reading': 0,
    'lat_reading': 0,
    'lon_reading': 0,
    'speed_reading' :0,
    'gps_heading_reading': 0,
    'jet1_temp': 0,
    'jet2_temp': 0,
    'compartment_temp': 0,
    'gps_distance': 0,
    'jet1_current': 0, #starboard
    'jet2_current': 0, #port
    'pack_voltage': 0,
    'vector': 0,
    'magnitude': 0,
    'gyro_z': 0,
    'kalman_lp': 0,
    'kalman': 0,
}

# Save the Log Folder location
log_location = '/home/pi/coms-common/logs'
# Save the Initial Log file Name 
log_filename = 'log'
# Set the logger to wait by default
running = False

class Logger :

    def __init__(self):
        # Save the State for each log entry

        # Set the Default Subscriptons for Logging
        self.default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/adc" : on_adc_received,
            "/status/internal_compass" : on_internal_compass_received,
            "/status/temp" : on_temp_received,
            "/status/vector" : on_vector_received,
            # For Commands Sent by the Web Interface
            "/command/log/name" : on_log_name,
            "/command/log/startstop" : on_log_startstop,
        }

        # Create a Subcriber to get all the date
        self.subber = Subscriber(client_id="loggertest", broker_ip="192.168.1.170", default_subscriptions=self.default_subscriptions)
        self.subber.client.loop_start()
        # thread = Thread(target=self.subber.listen)
        # thread.start()

        
    def run_once(self):
        global running
        global log_location
        global log_filename

        if running:
            with open(f"{log_location}/{log_filename}.txt", "a+") as outfile:
                json.dump(curr_state, outfile)
                outfile.write("\n")


def on_log_name(client, userdata, message):
    global log_filename

    obj = json.loads(message.payload.decode('utf-8'))
    
    log_title = obj['name']
    time = datetime.today()
    log_time = (
        f"{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}"
    )
    # Reset the Current Log File
    log_filename = log_title + "_" + log_time
    
    print(f'Log title updated to : {log_filename}')
    # print("received")
    # exists = True
    # exists_message = {
    #     'exists' : exists
    # }
    # app_json = json.dumps(exists_message)
    # pubber.publish("/status/log_exists", app_json)
    # print(exists_message)
    # exists = False

def on_log_startstop(client, userdata, message):
    global running

    obj = json.loads(message.payload.decode('utf-8'))
    running = bool(obj['running'])
    print(f'The Log start came in as type : {type(running)} was : {obj["running"]}')
    print(f'Logging Running : {running}')
    
def on_temp_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['jet1_temp'] = obj["jet1_temp"]
    curr_state['jet2_temp'] = obj["jet2_temp"]
    curr_state['compartment_temp'] = obj["compartment_temp"]

def on_compass_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['mag_compass_reading'] = obj['compass']
    curr_state['gyro_z'] = obj['gyro_z']
    curr_state['kalman_lp'] = obj['kalman_lp']
    curr_state['kalman'] = obj['kalman']

def on_internal_compass_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['int_compass_reading'] = obj['heading']

def on_gps_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['time_reading'] = obj["time"]
    curr_state['lat_reading'] = obj['latitude']
    curr_state['lon_reading'] = obj['longitude']
    curr_state['speed_reading'] = obj["speed"]
    curr_state['gps_heading_reading'] = obj["course"]
    curr_state['gps_distance'] = obj['distance']

def on_adc_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['jet1_current'] = obj["jet1_amps"]
    curr_state['jet2_current'] = obj["jet2_amps"]
    curr_state['pack_voltage'] = obj["pack_voltage"]

def on_vector_received(client, userdata, message):
    global curr_state

    obj = json.loads(message.payload.decode('utf-8'))

    curr_state['vector'] = obj["heading"]
    curr_state['magnitude'] = obj["magnitude"]
