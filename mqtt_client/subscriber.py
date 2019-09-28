from mqtt_client.client import MQTTClient

class Subscriber():

    def __init__(self, client_id="default_subscriber", default_subscriptons=None):

        # Define Broker IP Address
        broker_ip = "192.168.1.102"

        self.client = MQTTClient(mqtt_client_id=client_id, broker_address=broker_ip)


    def subscribe_many(self, subscriptions):
        print(subscriptions)
        for topic, callback in subscriptions.items():
            self.subscribe(topic, callback)

    def subscribe(self, topic, callback=None):
        self.client.subscribe(topic)
        if callback is not None:
            self.client.message_callback_add(topic, callback)


    def listen(self):
        self.client.loop_forever()
