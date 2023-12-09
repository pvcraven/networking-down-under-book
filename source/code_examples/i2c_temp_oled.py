"""
This prints the temp and humidity from the AHT20 sensor
available frokm Adafruit.

Before you use this program, you'll need to install the 
Adafruit library with:
pip3 install adafruit-circuitpython-ahtx0
pip3 install adafruit-circuitpython-ssd1306
"""
import time
import datetime
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ahtx0
import adafruit_ssd1306

# You'll need to put the OLED screen's address here.
# You can see current addresses with:
# sudo i2cdetect -y 1
OLED_DEVICE_ADDRESS = 0x3D

# Change these to the right size for your display!
OLED_WIDTH = 128
OLED_HEIGHT = 64 

def setup_aht20():
    # Create sensor object, communicating over the board's default I2C bus
    # uses board.SCL and board.SDA
    i2c = board.I2C()  
    sensor = adafruit_ahtx0.AHTx0(i2c)
    return sensor


def setup_oled():
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Use for I2C.
    i2c = board.I2C()

    oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, 
                                        OLED_HEIGHT, 
                                        i2c, 
                                        addr=OLED_DEVICE_ADDRESS, 
                                        reset=oled_reset)
    return oled


def get_readings(sensor):
        temp_c = sensor.temperature
        temp_f = temp_c * (9.0 / 5.0) + 32.0
        humidity = sensor.relative_humidity
        return temp_f, humidity


def display_text(oled, line_1, line_2, line_3):

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Load a font.
    # font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/FreeSans.ttf", size=17)

    # Draw the text
    draw.text((0, 0), line_1, font=font, fill=255)
    draw.text((0, 23), line_2, font=font, fill=255)
    draw.text((0, 45), line_3, font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show() 


def run_display_loop(sensor, oled):
    while True:
        try:
            temp_f, humidity = get_readings(sensor)

            line_1 = "Time: " + datetime.datetime.now().strftime("%I:%M %p")
            line_2 = f"Temp: {temp_f:4.1f} F"
            line_3 = f"Humidity: {humidity:4.1f}%"

            display_text(oled, line_1, line_2, line_3)

        except OSError as error:
            print(f"Error reading data: {error}")

        time.sleep(2)


def main():
    sensor = setup_aht20()
    oled = setup_oled()

    run_display_loop(sensor, oled)



main()
