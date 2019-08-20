import paho.mqtt.client as mqtt #import the client1
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


broker_address="192.168.1.7" 
#broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("P1") #create new instance
# Attach a message received callback
client.on_message = on_message

print("connecting to broker")
# COnnect to the broker
client.connect(broker_address)

# Start the Loop
client.loop_start()


print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")

print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")

# Wait for the broker to retur the message
time.sleep(4)

# STop the Loop 
client.loop_stop()

