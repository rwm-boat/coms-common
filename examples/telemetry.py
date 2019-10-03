from mqtt_client.publisher import Publisher

pubber = Publisher(client_id="log_command", broker_ip="192.168.1.170")

while True:
    # Wait for the broker to retur the message
    log_title = input("Enter the log filename base: ")
    pubber.publish("/command/logging", str(log_title))
