from mqtt_client.subscriber import Subscriber
import json
import time


def on_time_received(client, userdata, message):
    send_time = float(message.payload.decode("utf-8"))
    recv_time = time.time() * 1000
    time_in_transit = recv_time - send_time
    print(f"Message received  {message.payload.decode('utf-8')}")
    print(f"Transit Time: {time_in_transit} Milliseconds")


def on_gps_received(client, userdata, message):
    #print("RECEIVED GPS DATA")
    obj = json.loads(message.payload.decode('utf-8'))
    print("time: " + str(obj['time']))
    print("latitude" + str(obj['latitude']))
    print("longitude" + str(obj['longitude']))
   
# ==================
# -- MAIN METHOD -- 
# ==================
if __name__ == '__main__':

    default_subscriptions = {
        "/status/time": on_time_received,
        "/status/gps": on_gps_received
    }
     
    subber = Subscriber(client_id="test_subber", broker_ip="127.0.0.1", default_subscriptions=default_subscriptions)
    
    # subber.subscribe("/status/time", on_time_received)
    # subber.subscribe("/status/gps", on_gps_received)
    # subber.subscribe_many(default_subscriptions)

    subber.listen()

    while(True):
        # Wait for the broker to retur the message
        time.sleep(1)

