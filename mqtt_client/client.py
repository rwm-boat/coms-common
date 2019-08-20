import paho.mqtt.client as mqtt #import the client1
import time


class MQTTClient(mqtt.Client):

    def __init__(self, client_id="", broker_address="pi-zero", on_connect = None, on_message_received= None):
        
        super().__init__(client_id)

        # Set the Initial Callbacks
        if on_connect: 
            self.on_connect = on_connect
        else: 
            self.on_connect = self._on_connect
        if on_message_received:     
            self.on_message = on_message_received
        else: 
            self.on_message= self._on_message_received

        # Connect to the Broker
        print(f"Attempting to conect to broker at {broker_address}")
        self.connect(broker_address)
        print("Successfully Connected to Broker")
        # Maintain Connection
        #self.loop_forever()


    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect(self, client, userdata, flags, rc, default_subs=[]):
        print("Connected to Broker with result code "+str(rc))


        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic in default_subs:
            client.subscribe(topic)


    # The callback for when a PUBLISH message is received from the server.
    def _on_message_received(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def subscribe_to_topic(self, topic):
        self.subscribe(topic)

    def publish_message(self, topic, message):
        self.publish(topic, message)
    



# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    broker_address="192.168.1.7" 

    print("creating new instance")
    client = MQTTClient("P1", broker_address) #create new instance


    print("Subscribing to topic")
    client.subscribe_to_topic("status/temp_senesor/celcius")

    print("Publishing message")
    client.publish_message("status/temp_senesor/celcius","temp: 25")

    # Wait for the broker to retur the message
    time.sleep(4)

   

