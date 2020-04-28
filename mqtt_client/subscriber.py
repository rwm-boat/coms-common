from mqtt_client.client import MQTTClient

class Subscriber():

    def __init__(self, client_id="default_subscriber", broker_ip="192.168.8.170", default_subscriptions=None):        
        self.client = MQTTClient(mqtt_client_id=client_id, broker_address=broker_ip)
        if default_subscriptions is not None:
            self.subscribe_many(default_subscriptions)


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
