"""Cherrypy tutorial.

Tutorial 1: A basic web application
Tutorial 2: Different URLs lead to different functions
Tutorial 3: My URLs have parameters
Tutorial 4: Submit this form
Tutorial 5: Track my-end-user's activity
Tutorial 6: What about my javascripts, CSS and images?
Tutorial 7: Give us a REST
Tutorial 8: Make it smoother with Ajax
Tutorial 9: Data is all my life
Tutorial 10: Make it a modern single-page application with React.js
"""
import os
import os.path
import random
import sqlite3
import string
import time

import cherrypy


DB_STRING = "my.db"

class StringGenerator:
    @cherrypy.expose
    def index(self):
        fname= os.path.join(os.path.dirname(__file__), "public", "index.html")
        return open(fname)

@cherrypy.expose
class StringGeneratorWebService:
    @cherrypy.tools.accept(media="text/plain")
    def GET(self):
        with sqlite3.connect(DB_STRING) as conn:
            cherrypy.session["ts"] = time.time()
            rv = conn.execute(
                "SELECT value FROm user_string WHERE session_id=?",
                (cherrypy.session.id,)
            )
            return rv.fetchone()
    
    def POST(self, length=8):
        text = "".join(random.sample(string.hexdigits, int(length)))
        with sqlite3.connect(DB_STRING) as conn:
            cherrypy.session["ts"] = time.time()
            conn.execute(
                "INSERT INTO user_string VALUES(?, ?)",
                (cherrypy.session.id, text)
            )
        return text
    
    def PUT(self, other_txt):
        with sqlite3.connect(DB_STRING) as conn:
            cherrypy.session["ts"] = time.time()
            conn.execute(
                "UPDATE user_string SET value=? WHERE session_id=?",
                (other_txt, cherrypy.session.id)
            )

    def DELETE(self):
        cherrypy.session.pop("mystring", None)
        with sqlite3.connect(DB_STRING) as conn:
            conn.execute(
                "DELETE FROm user_string WHERE session_id=?",
                (cherrypy.session.id,)
            )


def setup_database():
    """Create the `user_string` table in the database on server startup."""
    with sqlite3.connect(DB_STRING) as conn:
        conn.execute("CREATE TABLE user_string (session_id, value)")


def cleanup_database():
    """Destroy the `user_string` table from the database on server shutdown."""
    with sqlite3.connect(DB_STRING) as conn:
        conn.execute("DROP TABLE user_string")


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

    cherrypy.engine.subscribe("start", setup_database)
    cherrypy.engine.subscribe("stop", cleanup_database)
    
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, "/", conf)
