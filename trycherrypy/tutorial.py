"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
Tutorial 4: Submit this form
Tutorial 5: Track my-end-user's activity
"""
import random
import string

import cherrypy


class StringGenerator:
    @cherrypy.expose
    def index(self):
        return """<html>
            <head></head>
            <body>
                <form method="get" action="generate">
                    <label for="length">Length</label>
                    <input type="text" value="8" name="length" />
                    <button type="submit">Give it now!</button>
                </form>
            </body>
        </html>"""
    
    @cherrypy.expose
    def generate(self, length=8):
        text = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session["mystring"] = text
        return text
    
    @cherrypy.expose
    def display(self):
        return cherrypy.session["mystring"]


if __name__ == "__main__":
    conf = {
        "/": {
            "tools.sessions.on": True
        }
    }
    cherrypy.quickstart(StringGenerator(), "/", conf)
