"""
Demo for Adafruit's OLED display:
https://www.adafruit.com/product/326

Before running, install the library with:
pip3 install adafruit-circuitpython-ssd1306
"""

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# You'll need to put the OLED screen's address here.
# You can see current addresses with:
# sudo i2cdetect -y 1
OLED_DEVICE_ADDRESS = 0x3D

# Change these to the right size for your display!
OLED_WIDTH = 128
OLED_HEIGHT = 64 

BORDER = 5


def setup_oled():
    # Set up i2c
    i2c = board.I2C()

    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Connect to device
    oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, 
                                        OLED_HEIGHT, 
                                        i2c, 
                                        addr=OLED_DEVICE_ADDRESS, 
                                        reset=oled_reset)

    return oled


def create_image(text):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image_size = (OLED_WIDTH, OLED_HEIGHT)
    image = Image.new("1", image_size)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    rect = (0, 0, OLED_WIDTH, OLED_HEIGHT)
    draw.rectangle(rect, outline=255, fill=255)

    # Draw a smaller inner rectangle
    rect = (BORDER, 
            BORDER, 
            OLED_WIDTH - BORDER - 1, 
            OLED_HEIGHT - BORDER - 1)
    draw.rectangle(rect, outline=0, fill=0)

    # Load default font.
    font = ImageFont.load_default()

    # Draw Some Text
    font_width, font_height = font.getsize(text)
    position = (OLED_WIDTH // 2 - font_width // 2, 
                OLED_HEIGHT // 2 - font_height // 2)
    draw.text(position, text, font=font, fill=255)

    return image


def main():
    try:
        oled = setup_oled()
    except ValueError as error:
        # Error getting sensor
        print(f"Error, unable to find the OLED screen.")
        print(f"{error}")
        print(f"Make sure it is plugged in and run 'sudo i2cdetect -y 1' to verify.")
        return

    image = create_image("Hello World!")

    # Display image
    oled.image(image)
    oled.show()

main()
