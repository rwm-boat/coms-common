import paho.mqtt.client as mqtt 

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
        payload = str(message.payload.decode("utf-8"))
        print(f"message received  {payload}")
        print(f"message topic= {message.topic}")
        print(f"message qos= {message.qos}")
        print(f"message retain flag= {message.retain}")
        
    
    def _on_publish_ret(self, client, userdata, mid):
        print(f"Message Published with mid : {str(mid)}")


    def _on_subscribe_ret(self, client, userdata, mid, granted_qos):
        print(f"Subscribed to topic with mid : {str(mid)} granted quality of service : {granted_qos}")


    def _on_unsubscribe_ret(self, client, userdata, mid):
        print(f"Subscribed to topic with mid : {str(mid)}")


