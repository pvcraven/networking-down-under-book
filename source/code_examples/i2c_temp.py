"""
This prints the temp and humidity from the AHT20 sensor
available frokm Adafruit.
https://www.adafruit.com/product/4566

Before you use this program, you'll need to install the 
Adafruit library with:
pip3 install adafruit-circuitpython-ahtx0
"""
import time
import board
import adafruit_ahtx0


def setup_aht20():
    # Create sensor object, communicating over the board's default I2C bus
    # uses board.SCL and board.SDA
    i2c = board.I2C()
    sensor = adafruit_ahtx0.AHTx0(i2c)
    return sensor


def get_readings(sensor):
        temp_c = sensor.temperature
        temp_f = temp_c * (9.0 / 5.0) + 32.0
        humidity = sensor.relative_humidity
        return temp_f, humidity


def run_display_loop(sensor):
    while True:
        try:
            temp_f, humidity = get_readings(sensor)
            print(f"Temp: {temp_f:4.1f} F, Humidity: {humidity:4.1f}%")
        except OSError as error:
            print(f"Error reading data: {error}")

        time.sleep(2)


def main():
    
    try:
        # Try to get the sensor
        sensor = setup_aht20()
    except ValueError as error:
        # Error getting sensor
        print(f"Error, unable to find the sensor.")
        print(f"{error}")
        print(f"Make sure it is plugged in and run 'sudo i2cdetect -y 1' to verify.")
        return

    run_display_loop(sensor)


main()
