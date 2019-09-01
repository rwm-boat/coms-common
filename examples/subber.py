import sys
import time
import argparse

from mqtt_client.client import MQTTClient

def on_time_received(client, userdata, message):
    send_time = float(message.payload.decode("utf-8"))
    recv_time = time.time() * 1000
    time_in_transit = recv_time - send_time
    print(f"Message received  {message.payload.decode('utf-8')}")
    print(f"Transit Time: {time_in_transit} Milliseconds")


def on_gps_received(client, userdata, message):
    print("RECEIVED GPS DATA")


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
        client_id = "dummy_subber"
        print(f"No Client ID provided, set to {client_id}")
  
    #create new instance
    #create new instance
    #client = MQTTClient(mqtt_client_id=client_id, transport="tcp", broker_address=broker_address, on_message_ret=on_time_received) 
    client = MQTTClient(mqtt_client_id=client_id, transport="tcp", broker_address=broker_address) 
    
    # Setup Time Topic
    client.subscribe_to_topic("status/time")
    client.add_specific_callback("/status/time", on_time_received)
    
    client.loop_forever()

    # Setup GPS Topic
    client.subscribe_to_topic("status/gps")
    client.add_specific_callback("/status/time", on_gps_received)



    while(True):
        # Wait for the broker to retur the message
        time.sleep(.001)
    #client.publish_message("status/temp_senesor/celcius","temp: 25")

