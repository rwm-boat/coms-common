from threading import Thread
from logger import Logger
import time

boat_log = Logger()

# Do the rest of your service after this point, you'll be running as 'pi'
while True:
    # This is where the main work of your service should go
    boat_log.run_once()
    time.sleep(0.1)


# l = Logger()
# # Start The logger
# thread = Thread(target=l.run)
# thread.start()
