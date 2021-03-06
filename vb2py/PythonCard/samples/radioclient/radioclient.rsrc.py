{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'RadioClient PythonCard Application',
          'size':(464, 494),
          'statusBar':1,
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuRadio',
             'label':'Radio',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuRadioGetRecentPosts',
                   'label':'Get Recent Posts',
                   'command':'radioGetRecentPosts',
                  },
                  {'type':'MenuItem',
                   'name':'menuRadioNewPost',
                   'label':'New Post',
                   'command':'radioNewPost',
                  },
                  {'type':'MenuItem',
                   'name':'menuRadioEditPost',
                   'label':'Upload Selected Post',
                   'command':'radioEditPost',
                  },
                  {'type':'MenuItem',
                   'name':'menuRadioDeletePost',
                   'label':'Delete Selected Post',
                   'command':'radioDeletePost',
                  },
                  {'type':'MenuItem',
                   'name':'menuRadioGetTemplate',
                   'label':'Get Template',
                   'command':'radioGetTemplate',
                  },
                  {'type':'MenuItem',
                   'name':'menuRadioSetTemplate',
                   'label':'Set Template',
                   'command':'radioSetTemplate',
                  },
                  { 'type':'MenuItem', 'name':'radioSep1', 'label':'-' },
                  {'type':'MenuItem',
                   'name':'menuRadioPreviewPost',
                   'label':'Preview Selected Post\tCtrl+P',
                   'command':'radioPreviewPost',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuOptions',
             'label':'Options',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuOptionsAutoComplete',
                   'label':'Shell AutoComplete\tCtrl+1',
                   'checkable':1,
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Button', 
    'name':'btnRecentPosts', 
    'position':(4, 2), 
    'command':'radioGetRecentPosts', 
    'label':'Recent Posts', 
    },

{'type':'Button', 
    'name':'btnNewPost', 
    'position':(92, 2), 
    'command':'radioNewPost', 
    'label':'New Post', 
    },

{'type':'Button', 
    'name':'btnPreviewPost', 
    'position':(172, 2), 
    'size':(79, -1), 
    'command':'radioPreviewPost', 
    'label':'Preview Post', 
    },

{'type':'Button', 
    'name':'btnEditPost', 
    'position':(258, 2), 
    'command':'radioEditPost', 
    'default':1, 
    'label':'Upload Selected Post', 
    },

{'type':'List', 
    'name':'listPosts', 
    'position':(-2, 30), 
    'size':(381, 137), 
    'items':[], 
    },

{'type':'TextArea', 
    'name':'fldContent', 
    'position':(-4, 186), 
    'size':(380, 213), 
    'font':{'size': 9, 'faceName': 'Courier New', 'family': 'monospace'}, 
    },

] # end components
} # end background
] # end backgrounds
} }
