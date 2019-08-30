import paho.mqtt.client as mqtt 

import time
import argparse
import logging


class MQTTClient(mqtt.Client):

    def __init__(self, mqtt_client_id="", transport="tcp", broker_address="pi-zero", on_connect_ret=None, on_disconnect_ret=None, on_message_ret=None, on_publish_ret=None, on_subscribe_ret=None, on_unsubscribe_ret=None):
        
        super().__init__(client_id=mqtt_client_id)

        # Set the Initial Callbacks
        if on_connect_ret is not None: 
            self.on_connect = on_connect_ret
        else: 
            self.on_connect = self._on_connect_ret
            
        if on_disconnect_ret is not None: 
            self.on_disconnect = on_disconnect_ret
        else: 
            self.on_disconnect = self._on_disconnect_ret

        if on_message_ret is not None:     
            self.on_message = on_message_ret
        else: 
            self.on_message = self._on_message_ret

        if on_publish_ret is not None:     
            self.on_publish = on_publish_ret
        else: 
            self.on_publish = self._on_publish_ret
    
        if on_subscribe_ret is not None:     
            self.on_subscribe = on_subscribe_ret
        else: 
            self.on_subscribe = self._on_subscribe_ret

        if on_unsubscribe_ret is not None:     
            self.on_unsubscribe = on_unsubscribe_ret
        else: 
            self.on_unsubscribe = self._on_unsubscribe_ret

        # Connect to the Broker
        self.connect_to_broker(broker_address)


    # Connects to the Boat Broker at given IP / hostname
    def connect_to_broker(self, broker_address):
        try:
            print(f"Attempting to conect to broker at {broker_address}")
            self.connect(broker_address)
        except:
            print(f"Faled to connect to broker at : {broker_address}")
        else:
            print(f"Successfuly connected to broker at : {broker_address}")


    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect_ret(self, client, userdata, flags, rc):
        print(f"Connected to Broker with result code : {str(rc)}")

    # Called when the client disconnects from the broker.
    def _on_disconnect_ret(self, client, userdata, rc):
        print(f"Disconnected from Server with result code : {str(rc)}")

    ## 
    # Called when a message has been received on a topic that the client subscribes to 
    #  and the message does not match an existing topic filter callback. 
    #  Use message_callback_add() [ add_specific_callback() ] to define a callback that will 
    #  be called for specific topic filters. on_message will serve as fallback when none matched.
    def _on_message_ret(self, client, userdata, message):
        # payload = str(message.payload.decode("utf-8"))
        # print(f"message received  {payload}")
        # print(f"message topic= {message.topic}")
        # print(f"message qos= {message.qos}")
        # print(f"message retain flag= {message.retain}")
        payload = str(message.payload.decode("utf-8"))
        temp = payload.split(" ")
        send_time = float(temp[-1])
        recv_time = time.time() * 1000
        time_in_transit = recv_time - send_time
        print(f"message received  {payload}")
        print(f"Transit Time: {time_in_transit} Milliseconds")

    ###
    # This function allows you to define callbacks that handle incoming messages
    #  for specific subscription filters, including with wildcards. This lets you, 
    #  for example, subscribe to sensors/# and have one callback to handle sensors/temperature 
    #  and another to handle sensors/humidity
    def add_specific_callback(self, topic_filter, callback):
        message_callback_add(topic_filter, callback)

    
    # Remove a topic/subscription specific callback previously registered
    #  using message_callback_add() [ add_specific_callback() ]
    def remove_secific_callback(self, topic_filter):
        message_callback_remove(topic_filter)

    
    def _on_publish_ret(self, userdata, mid):
        print(f"Message Published with mid : {str(mid)}")


    def _on_subscribe_ret(self, client, userdata, mid, granted_qos):
        print(f"Subscribed to topic with mid : {str(mid)} granted quality of service : {granted_qos}")


    def _on_unsubscribe_ret(self, client, userdata, mid):
        print(f"Subscribed to topic with mid : {str(mid)}")


    def subscribe_to_topic(self, topic):
        self.subscribe(topic)

    def publish_message(self, topic, message):
        self.publish(topic, message)
    

def on_time_received(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    temp = payload.split(" ")
    send_time = temp[-1]
    recv_time = time.time() * 1000
    time_in_transit = recv_time - send_time
    print(f"message received  {payload}")
    print(f"Transit Time: {time_in_transit} Milliseconds")


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
    client.subscribe_to_topic("status/time")

    while(True):
        # Wait for the broker to retur the message
        time.sleep(.001)
    #client.publish_message("status/temp_senesor/celcius","temp: 25")

    client.loop_stop()

   

