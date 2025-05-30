# micropython code for BME 280
'''
This code reads the temperature, pressure and humidity from the BME280 sensor 
and prints the values to the console.

On PyPi you will install "micropython-bme280" library.

References:
- https://electrocredible.com/raspberry-pi-pico-bme280-interfacing-guide-using-micropython/
- https://microcontrollerslab.com/bme280-raspberry-pi-pico-micropython-tutorial/
'''

from time import sleep, ticks_ms, ticks_diff
import utime
from sensors import read_dht_sensor
from mpc import run_mpc
from datastream import send_data_to_pc, connect_wifi

# Constants
MEASUREMENT_INTERVAL = 600000  # 10 minutes in milliseconds
server_url = "https://abcd1234.ngrok.io/receive-data" #TODO placeholder url

# Variables
last_measurement_time = ticks_ms()

# Connect to Wi-Fi

# Create and activate the WLAN interface
import network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Get mac address
from datastream import get_mac_address, print_mac_address
mac_address = get_mac_address()
print_mac_address()  # Print the MAC address for reference

#define ssid and password for wifi connection
ssid = 'CMU-DEVICE'
password = ''

connect_wifi(ssid, password)

#Measure once before looping
timestamp = utime.time()
timestamp_f = "{}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
    utime.localtime()[0],  # Year
    utime.localtime()[1],  # Month
    utime.localtime()[2],  # Day
    utime.localtime()[3],  # Hour
    utime.localtime()[4],  # Minute
    utime.localtime()[5])   # Second

temperature, humidity = read_dht_sensor(2)
data = {
    "timestamp": timestamp_f,
    "temperature": temperature,
    "dht22_humidity": humidity,
}

#measure every 10 minutes
while True:
    current_time = ticks_ms()

    # Check if it's time to read the sensors
    if ticks_diff(current_time, last_measurement_time) >= MEASUREMENT_INTERVAL:
        # Read data from DHT sensor
        temperature, humidity = read_dht_sensor(2)
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            # Send data to PC
            timestamp = utime.time()
            timestamp_f = "{}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
            utime.localtime()[0],  # Year
            utime.localtime()[1],  # Month
            utime.localtime()[2],  # Day
            utime.localtime()[3],  # Hour
            utime.localtime()[4],  # Minute
            utime.localtime()[5])   # Second
            
            data = {
                "timestamp": timestamp_f,
                "temperature": temperature,
                "dht22_humidity": humidity,
            }
            #TODO send_data_to_pc(data)
        else:
            print("Failed to read sensor data.")
        
        # Update the last measurement time
        last_measurement_time = current_time

    # Run the model predictive control logic
    # TODO mpc_result = run_mpc()
    #TODO print(f"MPC Result: {mpc_result}")

    # Sleep for a short time to avoid busy-waiting
    sleep(1)
