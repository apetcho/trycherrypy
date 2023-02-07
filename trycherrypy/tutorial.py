"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
Tutorial 4: Submit this form
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
        return "".join(random.sample(string.hexdigits, int(length)))


if __name__ == "__main__":
    cherrypy.quickstart(StringGenerator())
