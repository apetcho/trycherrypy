"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
"""
import random
import string

import cherrypy


class StringGenerator:
    @cherrypy.expose
    def index(self):
        return "Hello world!"
    
    @cherrypy.expose
    def generate(self, length=8):
        return "".join(random.sample(string.hexdigits, int(length)))


if __name__ == "__main__":
    cherrypy.quickstart(StringGenerator())
