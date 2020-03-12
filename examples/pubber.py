from mqtt_client.publisher import Publisher
import time


# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    pubber = Publisher(client_id="time_pubber",  broker_ip="192.168.1.170")

    while(True):
        milli = time.time() * 1000
        pubber.publish("/status/time",str(milli))
        #time.sleep(.01)
