from mqtt_client.publisher import Publisher

import time

# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':
    
    # Create a New Pubilser
    pubber = Publisher(client_id="gps_pubber")

    while(True):
        coords  = [1, 1, 1]
        pubber.publish("/status/gps",str(coords))
        time.sleep(.20)

