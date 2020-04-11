"""A simple server to convert files from VB to Python"""

import vbparser
import parserclasses
import converter
import config
import json
import re
import os
import tempfile
import utils
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
    def convertSingleFile(text, container=None, style='vb', returnpartial=True, dialect='VB6'):
        """Convert a single file of text"""
        if container is None:
            container = parserclasses.VBModule()
        ConversionHandler.setPythonic(style)
        ConversionHandler.clearHistory()
        try:
            return vbparser.convertVBtoPython(text, container, returnpartial=returnpartial, dialect=dialect)
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
            Config.setLocalOveride("Select", "SelectVariablePrefix", "select_variable_")
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
    return singleModule(parserclasses.VBModule(), parserclasses.VBDotNetModule())


@app.route('/single_class_module', methods=['POST'])
def singleClassModule():
    """Return a class module converted"""
    return singleModule(parserclasses.VBClassModule(), parserclasses.VBDotNetModule())


@app.route('/single_form_module', methods=['POST'])
def singleFormModule():
    """Return a form module converted"""
    return singleModule(parserclasses.VBFormModule(), parserclasses.VBDotNetModule())

@app.route('/submit_file', methods=['POST'])
def submitFile():
    """Submit a file as a test"""
    return storeSubmittedFile()


def singleModule(module_type, dot_net_module_type):
    """Convert a single module"""
    start_time = time.time()
    #
    # Failure information
    parsing_failed = False
    parsing_stopped_vb = None
    parsing_stopped_py = None
    #
    conversion_style = 'unknown'
    extra = ''
    line_count = -1
    language = 'UNKNOWN'
    version = converter.__version__
    #
    try:
        conversion_style = request.values['style']
        text = request.values['text']
        class_name = request.values.get('class_name', 'MyClass')
        failure_mode = request.values.get('failure-mode', 'line-by-line')
        requested_dialect = request.values.get('dialect', 'detect')
    except KeyError:
        result = 'No text or style parameter passed'
        status = 'FAILED'
    else:
        #
        language = requested_dialect if requested_dialect != 'detect' else detectLanguage(text)
        lines = text.splitlines()
        line_count = len(lines)
        if language != 'VB.NET':
            module_type.classname = class_name
            dialect = 'VB6'
        else:
            module_type = dot_net_module_type
            dialect = 'vb.net'
        module_type.classname = class_name
        #
        # Remove form stuff if it is there
        stripped_text = removeFormCruft(text)
        #
        try:
            try:
                if failure_mode == 'fail-safe':
                    utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'
                result = ConversionHandler.convertSingleFile(
                    stripped_text,
                    module_type,
                    conversion_style,
                    dialect=dialect,
                )
            finally:
                utils.BASE_GRAMMAR_SETTINGS['mode'] = 'line-by-line'
            status = 'OK'
        except Exception, err:
            result = str(err)
            status = 'ERROR'
        else:
            #
            # Check for errors and store them
            if failure_mode == 'fail-safe':
                match = re.match(".*UNTRANSLATED VB LINE.*", result, re.DOTALL)
            else:
                match = re.match(".*\(ParserError\).*?'(.*?)'", result, re.DOTALL)
            if match:
                parsing_failed = True
                if failure_mode == 'line-by-line':
                    parsing_stopped_vb = getLineMatch(match.groups()[0], text)
                    parsing_stopped_py = getLineMatch('(ParserError)', result)
                    parsing_stopped_vb += locateBadLine(text, parsing_stopped_vb)
                    extra = ' (parser failure after %5.2f%% of lines): [%s]' % (
                        100.0 * parsing_stopped_vb / line_count,
                        lines[parsing_stopped_vb]
                    )
                elif failure_mode == 'quick':
                    parsing_stopped_vb = 0
                    parsing_stopped_py = 0
                    extra = ' Quick fail mode'
                elif failure_mode == 'fail-safe':
                    parsing_stopped_vb, parsing_stopped_py = getErrorLinesBySafeMode(
                        text, result, module_type, conversion_style)
                    extra = ' Fail safe mode'

    #
    app.logger.info('[%s] Completed %d lines %s %s (%s) with status %s. Time took %5.2fs%s' % (
        request.remote_addr,
        line_count, module_type.__class__.__name__, conversion_style,
        language,
        status, time.time() - start_time, extra
    ))
    #
    result = json.dumps({
        'status': status,
        'result': result,
        'parsing_failed': parsing_failed,
        'parsing_stopped_vb': parsing_stopped_vb,
        'parsing_stopped_py': parsing_stopped_py,
        'language': language,
        'version': version,
    }, encoding='latin1')
    #
    # app.logger.info('[%s] Ended     %d lines %s %s' % (
    #     request.remote_addr,
    #     line_count, module_type.__class__.__name__, conversion_style,
    # ))
    #
    return result


def log_request(text):
    """Log the request

    A short term measure to debug server crashes.

    """
    handle, path = tempfile.mkstemp(prefix='vb2py_', suffix='.txt', dir='/tmp')
    f = os.fdopen(handle, 'w')
    f.write(text)
    f.close()
    return path


def getLineMatch(search, text):
    """Return the line partially matching the text"""
    for idx, line in enumerate(text.splitlines()):
        if search in line:
            return idx
    else:
        return 0


def storeSubmittedFile():
    """Store a file that was submitted"""
    vb = request.values['text']
    filename = time.strftime('%Y-%m-%d %H:%M:%S code.vb')
    full_path = os.path.join(utils.rootPath(), 'submitted_files', filename)
    app.logger.info('Storing file for testing as %s' % filename)
    with open(full_path, 'w') as f:
        f.write(vb)
    return json.dumps({
        'status': 'OK',
        'result': 'File stored for testing',
    })


def removeFormCruft(text):
    """Remove form stuff if it is there"""
    match = re.match('.*?^Begin.*?^End\s*$(.*)', text, re.DOTALL + re.MULTILINE)
    if match:
        app.logger.debug('Removed form information')
        stripped = match.groups()[0]
        return stripped
    else:
        return text


def locateBadLine(vb, error_line):
    """Given some vb with a parsing error at the line number, try to zoom in and get more precise

    We do this by parsing each line starting at the error to see which one fails.

    """
    for idx, line in enumerate(vb.splitlines()[error_line:]):
        try:
            parsed = vbparser.buildParseTree(line, 'isolated_single_line', returnpartial=False)
        except:
            return idx
    else:
        return 0


def detectLanguage(text):
    """Try to detect the underlying VB dialect"""
    flags = re.DOTALL + re.MULTILINE
    dot_net_signals = [
        re.compile('.*End Class.*', flags),
        re.compile('.*End Module.*', flags),
    ]
    for signal in dot_net_signals:
        if signal.match(text):
            return 'VB.NET'
    else:
        return 'VB6'


def getErrorLinesBySafeMode(vbtext, pytext, module_type, conversion_style):
    """Return all the failing lines using the safe mode approach"""
    untranslated = re.compile(r'.*?UNTRANSLATED VB LINE \[(.*?)\].*')
    py_lines = []
    vb_lines = []
    for py_line_num, line in enumerate(pytext.splitlines()):
        m = untranslated.match(line)
        if m:
            py_lines.append(py_line_num)
            vb_lines.append(getLineMatch(m.group(1), vbtext))
    return vb_lines, py_lines
