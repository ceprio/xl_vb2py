"""A simple server to convert files from VB to Python"""

import vbparser
import parserclasses
import config
import json
from flask import Flask, request
from flask_cors import CORS
import time


class ConversionError(Exception): """There was an error converting a line of text"""


#
# Logging config
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


app = Flask('VB2PY')
CORS(app)
Config = config.VB2PYConfig()
app.logger.info('Starting conversion server')


class ConversionHandler(object):
    """A server to convert files"""

    @staticmethod
    def convertSingleFile(text, container=None, style='vb'):
        """Convert a single file of text"""
        if container is None:
            container = parserclasses.VBModule()
        ConversionHandler.setPythonic(style)
        ConversionHandler.clearHistory()
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

    @staticmethod
    def clearHistory():
        """Reset any history in the parser

        The parser stores counters for things like select and with unique values
        and so this clears them out to ensure that each call gets a unique context.

        """
        parserclasses.VBSelect._select_variable_index = 0
        parserclasses.VBFor._for_variable_index = 0
        parserclasses.VBWith._with_variable_index = 0


@app.route('/test', methods=['GET', 'POST'])
def testResult():
    return json.dumps({'status': 'OK'})


@app.route('/single_code_module', methods=['POST'])
def singleCodeModule():
    """Return a code module converted"""
    app.logger.info('Code module conversion')
    return singleModule(parserclasses.VBModule())


@app.route('/single_class_module', methods=['POST'])
def singleClassModule():
    """Return a class module converted"""
    app.logger.info('Class module conversion')
    return singleModule(parserclasses.VBClassModule())


@app.route('/single_form_module', methods=['POST'])
def singleFormModule():
    """Return a form module converted"""
    app.logger.info('Form module conversion')
    return singleModule(parserclasses.VBFormModule())


def singleModule(module_type):
    """Convert a single module"""
    start_time = time.time()
    try:
        text = request.values['text']
        conversion_style = request.values['style']
    except KeyError:
        result = 'No text or style parameter passed'
        status = 'FAILED'
    else:
        app.logger.info('Starting conversion (%s) - %d lines' % (
            conversion_style, len(text),
        ))
        try:
            result = ConversionHandler.convertSingleFile(
                text,
                module_type,
                conversion_style,
            )
            status = 'OK'
        except Exception, err:
            result = str(err)
            status = 'ERROR'
    #
    app.logger.info('Completed with status %s. Time took %5.2fs' % (status, time.time() - start_time))
    #
    return json.dumps({
        'status': status,
        'result': result,
    })


