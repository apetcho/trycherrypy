"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
"""
import random
import string

import cherrypy


class StringGenerator:
    @cherrypy.expose
    def index(self):
        return "Hello world!"
    
    @cherrypy.expose
    def generate(self):
        return "".join(random.sample(string.hexdigits, 8))


if __name__ == "__main__":
    cherrypy.quickstart(StringGenerator())
