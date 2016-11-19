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

#cherrypy.quickstart(HelloWorld())
def start():
    cherrypy.tree.mount(HelloWorld(), '', None)
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()