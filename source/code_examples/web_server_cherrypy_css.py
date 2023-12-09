import os
import cherrypy
import random

# Serve static files out of the web subdirectory
PATH = os.path.abspath(os.path.dirname(__file__)) + "/web"


class WebServer(object):
    @cherrypy.expose
    def index(self):
        # Set the media type
        cherrypy.response.headers['Content-Type'] = 'text/html'
        random_number = random.randrange(1, 101)
        result = "<html>"
        result += "<head>"
        result += "<link rel='stylesheet' type='text/css' href='style.css'>"
        result += "</head>"
        result += "<body>"
        result += "<h1>My Page</h1>"
        result += f"<p>My random number: {random_number}</p>"
        result += "</body>"
        result += "</html>"

        return result


config = {
        '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH,
            },
    }

cherrypy.quickstart(WebServer(), config=config)
