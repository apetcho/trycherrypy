"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
Tutorial 4: Submit this form
Tutorial 5: Track my-end-user's activity
Tutorial 6: What about my javascripts, CSS and images?
Tutorial 7: Give us a REST
"""
# import os
# import os.path
import random
import string

import cherrypy


@cherrypy.expose
class StringGeneratorWebService:
    @cherrypy.tools.accept(media="text/plain")
    def GET(self):
        return cherrypy.session["mystring"]
    
    def POST(self, length=8):
        text = "".join(random.sample(string.hexdigits, int(length)))
        cherrypy.session["mystring"] = text
        return text
    
    def PUT(self, other_txt):
        cherrypy.session["mystring"] = other_txt

    def DELETE(self):
        cherrypy.session.pop("mystring", None)


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [
                ("Context-Type", "text/plain"),
            ],
        },
    }
    cherrypy.quickstart(StringGeneratorWebService(), "/", conf)
