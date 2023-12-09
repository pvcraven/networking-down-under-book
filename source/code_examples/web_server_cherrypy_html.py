import cherrypy
import random


class AdLib:
    @cherrypy.expose
    def index(self):

        # Set the media type
        cherrypy.response.headers['Content-Type'] = 'text/html'

        # Create some random lists to choose from
        career_list = ["barista", "astronaut", "doctor", "nurse",
                       "musician", "teacher", "application developer"]
        # Make the choices
        career = random.choice(career_list)

        # Print out the heading in HTML <h1> tags
        result = "<h1>Random Career Generator</h1>"

        # Write our story
        result += f"<p>When I graduate, I want to be a(n) {career}!</p>"

        # Return the result
        return result


cherrypy.quickstart(AdLib())
