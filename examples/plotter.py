import matplotlib.pyplot as plt
import json
import math


def load_old_log():
    time = []
    latitude = []
    longitude = []

    with open("log.txt", "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            time.append(obj["time"])
            if abs(obj["latitude"]) > error_filter:
                latitude.append(obj["latitude"])
            if abs(obj["longitude"]) > error_filter:
                longitude.append(obj["longitude"])
    return time, latitude, longitude


def plot_lat_long(latitude, longitude):
    plt.subplot(1, 2, 1)
    plt.plot(latitude, label="Latitude")
    plt.title("Latitude")
    plt.xlabel("Time")
    plt.ylabel("Coords")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(longitude, label="Longitude")
    plt.title("Longiude")
    plt.xlabel("Time")
    plt.ylabel("Coords")
    plt.legend()
    plt.grid()
    plt.show()


def print_lat_long_csv(latitude, longitude):
    with open("gps.csv", "w") as gps:
        gps.write("latitude,longitude\n")
        for i in range(0, len(latitude)):
            gps.write(f"{latitude[i]},{longitude[i]}\n")


def load_adc_log():
    value = []
    voltage = []

    with open("adc_log.txt", "r") as log_file:
        for line in log_file.readlines():
            obj = json.loads(line)
            value.append(obj["value"])
            voltage.append(obj["voltage"])
    return value, voltage


def load_compass_log():
    temp = []
    compass = []

    with open("compas_log.txt", "r") as log_file:
        for line in log_file.readlines():
            obj = json.loads(line)
            temp.append(obj["temp"])
            compass.append(obj["compass"])
    return temp, compass


def load_gps_log():
    time = []
    latitude = []
    longitude = []

    with open("gps_log.txt", "r") as log_file:
        error_filter = 20
        for line in log_file.readlines():
            obj = json.loads(line)
            time.append(obj["time"])
            if abs(int(obj["latitude"])) > error_filter:
                latitude.append(obj["latitude"])
            if abs(obj["longitude"]) > error_filter:
                longitude.append(obj["longitude"])
    return time, latitude, longitude


def plot_adc_log(value, voltage):
    plt.subplot(1, 2, 1)
    plt.plot(value, label="Value")
    plt.title("Value")
    plt.xlabel("Time")
    plt.ylabel("???")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(voltage, label="Voltage")
    plt.title("Voltage")
    plt.xlabel("Time")
    plt.ylabel("?????")
    plt.legend()
    plt.grid()
    plt.show()


def plot_compass_log(temp, compass):
    plt.subplot(1, 2, 1)
    plt.plot(temp, label="Temp")
    plt.title("Temp")
    plt.xlabel("Time")
    plt.ylabel("???")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(compass, label="Compass")
    plt.title("Compass")
    plt.xlabel("Time")
    plt.ylabel("?????")
    plt.legend()
    plt.grid()
    plt.show()


# ==================
# -- MAIN METHOD --
# ==================
if __name__ == "__main__":

    default_subscriptions = {
        # Nav Loggers
        "/status/gps": on_gps_received,
        "/status/compass": on_compass_received,
        # Jet Loggers
        "/status/temp": on_temp_received,
        "/status/adc": on_adc_received,
    }
    subber = Subscriber(
        client_id="logger_client",
        broker_ip="127.0.0.1",
        default_subscriptions=default_subscriptions,
    )
    subber.listen()

    while True:
        # Wait for the broker to retur the message
        log_title = input("Enter the log filename base: ")
        time = datetime.now()
        log_time = f"{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}:{time.microsecond}"
        _LOG_BASE = log_title + "_" + log_time

        # PLOT ADC
        # value, voltage = load_adc_log()
        # plot_adc_log(value, voltage)

        # PLOT NAV
        temp, compass = load_compass_log()
        time, latitude, longitude = load_gps_log()
        plot_compass_log(temp, compass)
        plot_lat_long(latitude, longitude)

        # load_old_log()
        # plot_lat_long()
        # print_lat_long_csv()

