"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
Tutorial 4: Submit this form
Tutorial 5: Track my-end-user's activity
Tutorial 6: What about my javascripts, CSS and images?
Tutorial 7: Give us a REST
Tutorial 8: Make it smoother with Ajax
"""
import os
import os.path
import random
import string

import cherrypy


class StringGenerator:
    @cherrypy.expose
    def index(self):
        fname= os.path.join(os.path.dirname(__file__), "public", "index.html")
        return open(fname)

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
            "tools.sessions.on": True,
            "tools.staticdir.root": os.path.abspath(os.path.dirname(__file__)),
        },
        "/generator": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "text/plain")],
        },
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./public",
        }
    }
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, "/", conf)
