"""A simple server to convert files from VB to Python"""

import vbparser
import SimpleHTTPServer
import SocketServer
import json
from flask import Flask, request
from flask_cors import CORS


class ConversionError(Exception): """There was an error converting a line of text"""


app = Flask('VB2PY')
CORS(app)

class ConversionHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """A server to convert files"""

    @staticmethod
    def convertSingleFile(text):
        """Convert a single file of text"""
        try:
            return vbparser.convertVBtoPython(text)
        except vbparser.VBParserError, err:
            raise ConversionError('Error converting VB. %s' % err)


@app.route('/test', methods=['GET', 'POST'])
def testResult():
    return json.dumps({'status': 'OK'})


@app.route('/single_module', methods=['POST'])
def singleModule():
    """Return a server"""
    try:
        text = request.values['text']
    except KeyError:
        result = 'No text parameter passed'
        status = 'FAILED'
    else:
        try:
            result = ConversionHandler.convertSingleFile(text)
            status = 'OK'
        except ConversionError, err:
            result = str(err)
            status = 'ERROR'
    #
    return json.dumps({
        'status': status,
        'result': result,
    })
