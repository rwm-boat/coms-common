from mqtt_client.publisher import Publisher
import json

pubber = Publisher(client_id="log_command", broker_ip="192.168.8.170")

while True:
    # Wait for the broker to retur the message
    command = str.lower(input("Enter the log filename base, `start`, or `stop` : "))

    # Check the start stop function
    if command == 'start':
        message = {
            'running': 1
        }
        print('Starting the Logger')
        pubber.publish("/command/log/startstop", json.dumps(message))
    elif command == 'stop':
        message = {
            'running': 0
        }
        print('Stopping the Logger')
        pubber.publish("/command/log/startstop", json.dumps(message))
    else:
        message = {
            'name': str(command)
        }
        print('Renaming the Log')
        pubber.publish("/command/log/name", json.dumps(message))


