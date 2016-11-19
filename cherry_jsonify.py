import cherrypy
import sys
from simplejson import JSONEncoder
encoder = JSONEncoder()

def jsonify_tool_callback(*args, **kwargs):
    response = cherrypy.response
    if (response.status < 400):
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Length'] = sys.getsizeof(response.body)
        response.body = encoder.iterencode(response.body)

cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30) 