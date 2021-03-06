{'application':{'type':'Application',
          'name':'jabberChat',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'jabberChat PythonCard Application',
          'size':(200, 150),
          'statusBar':1,
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileJoinConference',
                   'label':'Join Conference...',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSep1',
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
             'name':'menuStatus',
             'label':'Presence',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuStatusAvailable',
                   'label':'Available',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusDoNotDisturb',
                   'label':'Do Not Disturb',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusSep2',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusAway',
                   'label':'Away',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusBeRightBack',
                   'label':'Be Right Back',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusBusy',
                   'label':'Busy',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusNotAtHome',
                   'label':'Not At Home',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusNotAtMyDesk',
                   'label':'Not At My Desk',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusNotInTheOffice',
                   'label':'Not In The Office',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusOnThePhone',
                   'label':'On The Phone',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusOutToLunch',
                   'label':'Out To Lunch',
                   'command':'changeStatus',
                  },
                  {'type':'MenuItem',
                   'name':'menuStatusSteppedOut',
                   'label':'Stepped Out',
                   'command':'changeStatus',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuOptions',
             'label':'Options',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuOptionsShowWindow',
                   'label':'Show Incoming Message Window',
                   'checkable':1,
                   'checked':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsRaiseWindow',
                   'label':'Raise Incoming Message Window',
                   'checkable':1,
                  },
                  {'type':'MenuItem',
                   'name':'menuOptionsDisplayOfflineUsers',
                   'label':'Display Offline Users',
                   'checkable':1,
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'List', 
    'name':'listRoster', 
    'position':(0, 0), 
    'size':(250, 150), 
    'items':[], 
    },

] # end components
} # end background
] # end backgrounds
} }
