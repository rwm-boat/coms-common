from threading import Thread
from logger import Logger

l = Logger()
# Start The logger
thread = Thread(target=l.run)
thread.start()
