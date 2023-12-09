import cherrypy
import random

class AdLib:
    @cherrypy.expose
    def index(self):
        # Set the media type
        cherrypy.response.headers['Content-Type'] = 'text/plain'

        # Create some random lists to choose from
        career_list = ["barista", "astronaut", "doctor", "nurse",
                       "musician", "teacher", "application developer"]
        # Make the choices
        career = random.choice(career_list)

        # Print out the heading and a blank line
        result = "Random Career Generator\n"
        result += "\n"

        # Write our story
        result += f"When I graduate, I want to be a(n) {career}!\n"

        # Return the result
        return result

cherrypy.quickstart(AdLib())
