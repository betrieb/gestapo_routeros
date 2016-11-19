import cherrypy
import cherry_jsonify
from cherrypy import tools
from cherrypy import expose
import persistence

class HelloWorld(object):
    @expose
    def index(self):
        return "Running!"

    @tools.jsonify()
    @expose
    def data(self):
        return persistence.get_all()

cherrypy.quickstart(HelloWorld())