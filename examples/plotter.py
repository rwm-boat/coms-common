import matplotlib.pyplot as plt
import json
import math




time = []
latitude = []
longitude = []

with open('log.txt', 'r') as log_file:
    error_filter = 20
    for line in log_file.readlines():
        obj = json.loads(line)
        time.append(obj['time'])
        if abs(obj['latitude']) > error_filter:
            latitude.append(obj['latitude'])
        if abs(obj['longitude']) > error_filter:
            longitude.append(obj['longitude'])


plt.subplot(1, 2, 1)
plt.plot(latitude, label='Latitude')
plt.title('Latitude')
plt.xlabel('Time')
plt.ylabel('Coords')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(longitude, label='Longitude')
plt.title('Longiude')
plt.xlabel('Time')
plt.ylabel('Coords')
plt.legend()
plt.grid()
plt.show()

with open('gps.csv', 'w') as gps:
    gps.write("latitude,longitude\n")
    for i in range(0, len(latitude)):
        gps.write(f"{latitude[i]},{longitude[i]}\n")