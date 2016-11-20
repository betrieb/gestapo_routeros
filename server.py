import os.path
import cherrypy
import cherry_jsonify
from cherrypy import tools
from cherrypy import expose
import persistence

class HelloWorld(object):
    @expose
    def index(self):
        # return "Running!"
        raise cherrypy.HTTPRedirect("/html/index.html")

    @expose
    @tools.jsonify()
    def detail(self):
        return persistence.get_detail()
    
    @expose
    @tools.jsonify()
    def weekly(self):
        return persistence.get_by_week()

    @expose
    @tools.jsonify()
    def monthly(self):
        return persistence.get_by_month()

    @expose
    @tools.jsonify()
    def total(self):
        return persistence.get_by_host()


    @expose
    def html(self):
        return """<html>
        <head>
                <title>CherryPy static example</title>
                <link rel="stylesheet" type="text/css" href="css/style.css" type="text/css"></link>
                <script type="application/javascript" src="js/some.js"></script>
        </head>
        <body>
        <p>Static example</p>
        </body>
        </html>"""

#cherrypy.quickstart(HelloWorld())
def start():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {'/html': {  
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'html'), },
        }
        
    cherrypy.tree.mount(HelloWorld(), '', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    #cherrypy.config.update(conf)
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()

if __name__ == '__main__':
    start()
    cherrypy.engine.block()