import sys
import time

from ../mqtt_client/client import MQTTClient


# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--broker", help="The IP/hostname of the broker to connect to")
    parser.add_argument("-c", "--client", help="The Client ID to use with the broker")
    args = parser.parse_args()
    
    # Check the Broker IP Address
    if args.broker:
        broker_address = args.broker
    else:
        broker_address="192.168.1.70" 
        print(f"No Broker address provided, set to {broker_address}")

    # Check the Client ID
    if args.client:
        client_id = args.client
    else: 
        client_id = "dummy_client"
        print(f"No Client ID provided, set to {client_id}")
  
    #create new instance
    client = MQTTClient(mqtt_client_id=client_id, transport="tcp", broker_address=broker_address) 

    client.loop_start()

    while(True):
        milli = time.time() * 1000
        client.publish_message("status/time","time: " + str(milli))
        time.sleep(4)

    client.loop_stop()
