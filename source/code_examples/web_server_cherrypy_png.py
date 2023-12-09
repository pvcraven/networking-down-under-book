import cherrypy
import random
from PIL import Image
from PIL import ImageDraw
from io import BytesIO

WIDTH = 800
HEIGHT = 600

class AdLib:
    @cherrypy.expose
    def index(self):

        # Set the media type
        cherrypy.response.headers['Content-Type'] = 'image/png'

        # Create an image
        image = Image.new('RGB', (WIDTH, HEIGHT), color = 'white')

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Draw a bunch of random rectangles
        rectangle_count = 20
        for i in range(rectangle_count):
            x1 = random.randrange(WIDTH)
            y1 = random.randrange(HEIGHT)
            x2 = x1 + random.randrange(20, 80)
            y2 = y1 + random.randrange(20, 80)
            color = random.randrange(255), random.randrange(255), random.randrange(255)
            draw.rectangle([x1, y1, x2, y2], fill=color)

        # Convert image to bytes
        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        return byte_io.getvalue()


cherrypy.quickstart(AdLib())
