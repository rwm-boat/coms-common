from mqtt_client.client import MQTTClient

class Publisher():

    def __init__(self, client_id="default_publisher"):
        
        # Define Broker IP Address
        broker_ip = "192.168.1.70"

        self.client = MQTTClient(mqtt_client_id=client_id, broker_address=broker_ip)

    def publish(self, topic, message):
        self.client.publish(topic=topic, payload=message, retain=True)
