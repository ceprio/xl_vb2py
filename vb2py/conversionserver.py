"""A simple server to convert files from VB to Python"""

import vbparser
import parserclasses
import config
import json
from flask import Flask, request
from flask_cors import CORS


class ConversionError(Exception): """There was an error converting a line of text"""


app = Flask('VB2PY')
CORS(app)
Config = config.VB2PYConfig()


class ConversionHandler(object):
    """A server to convert files"""

    @staticmethod
    def convertSingleFile(text, container=None, style='vb'):
        """Convert a single file of text"""
        if container is None:
            container = parserclasses.VBModule()
        ConversionHandler.setPythonic(style)
        try:
            return vbparser.convertVBtoPython(text, container)
        except vbparser.VBParserError, err:
            raise ConversionError('Error converting VB. %s' % err)

    @staticmethod
    def setPythonic(style):
        """Set a pythonic configuration"""
        if style == 'vb':
            Config.setLocalOveride("General", "RespectPrivateStatus", "Yes")
            Config.setLocalOveride("Functions", "PreInitializeReturnVariable", "Yes")
            Config.setLocalOveride("Functions", "ReturnVariableName", "_ret")
            Config.setLocalOveride("Select", "SelectVariablePrefix", "_select")
            Config.setLocalOveride("With", "WithVariablePrefix", "_with")
        else:
            Config.setLocalOveride("General", "RespectPrivateStatus", "No")
            Config.setLocalOveride("Functions", "PreInitializeReturnVariable", "No")
            Config.setLocalOveride("Functions", "ReturnVariableName", "fn_return_value")
            Config.setLocalOveride("Select", "SelectVariablePrefix", "select_variable")
            Config.setLocalOveride("With", "WithVariablePrefix", "with_variable")


@app.route('/test', methods=['GET', 'POST'])
def testResult():
    return json.dumps({'status': 'OK'})


@app.route('/single_code_module', methods=['POST'])
def singleCodeModule():
    """Return a code module converted"""
    return singleModule(parserclasses.VBModule())


@app.route('/single_class_module', methods=['POST'])
def singleClassModule():
    """Return a class module converted"""
    return singleModule(parserclasses.VBClassModule())


def singleModule(module_type):
    """Convert a single module"""
    #
    # Set the type
    configuration = config.VB2PYConfig()

    try:
        text = request.values['text']
        conversion_style = request.values['style']
    except KeyError:
        result = 'No text or style parameter passed'
        status = 'FAILED'
    else:
        try:
            result = ConversionHandler.convertSingleFile(
                text,
                module_type,
                conversion_style,
            )
            status = 'OK'
        except ConversionError, err:
            result = str(err)
            status = 'ERROR'
    #
    return json.dumps({
        'status': status,
        'result': result,
    })


