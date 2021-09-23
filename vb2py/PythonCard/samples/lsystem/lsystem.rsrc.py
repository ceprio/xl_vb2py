{'application':{'type':'Application',
          'name':'Doodle',
    'backgrounds': [
    {'type':'Background',
          'name':'bgLSystem',
          'title':'L-System PythonCard Application',
          'size':(579, 550),
          'statusBar':1,
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileOpen',
                   'label':'&Open...\tCtrl+O',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSaveAs',
                   'label':'Save &As...',
                  },
                  {'type':'MenuItem',
                   'name':'fileSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuEdit',
             'label':'&Edit',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuEditCopy',
                   'label':'&Copy\tCtrl+C',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditPaste',
                   'label':'&Paste\tCtrl+V',
                  },
                  {'type':'MenuItem',
                   'name':'editSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditClear',
                   'label':'&Clear',
                   'command':'editClear',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuRender',
             'label':'&Render',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuRenderRenderNow',
                   'label':'&Render Now\tCtrl+R',
                   'command':'Render',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'TextField', 
    'name':'angleDisplay', 
    'position':(420, 25), 
    'size':(36, -1), 
    },

{'type':'StaticText', 
    'name':'StaticText2', 
    'position':(371, 29), 
    'text':'Angle:', 
    },

{'type':'Slider', 
    'name':'angle', 
    'position':(367, 54), 
    'size':(200, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':360, 
    'min':0, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':45, 
    },

{'type':'StaticText', 
    'name':'iterationDisplay', 
    'position':(435, 76), 
    },

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(368, 76), 
    'text':'Iterations:', 
    },

{'type':'Slider', 
    'name':'iterations', 
    'position':(364, 98), 
    'size':(200, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':10, 
    'min':1, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':3, 
    },

{'type':'Button', 
    'name':'btnRender', 
    'position':(1, 35), 
    'command':'Render', 
    'label':'Render', 
    },

{'type':'TextArea', 
    'name':'scriptField', 
    'position':(96, 0), 
    'size':(201, 118), 
    'text':'axiom=l\nl=+rf-lfl-fr+\nr=-lf+rfr+fl-', 
    },

{'type':'Button', 
    'name':'btnColor', 
    'position':(1, 67), 
    'label':'Color', 
    },

{'type':'BitmapCanvas', 
    'name':'bufOff', 
    'position':(0, 121), 
    'size':(568, 348), 
    'backgroundColor':(255, 255, 255), 
    },

] # end components
} # end background
] # end backgrounds
} }
