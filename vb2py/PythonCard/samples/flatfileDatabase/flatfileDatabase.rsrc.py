{'application':{'type':'Application',
          'name':'Addresses',
    'backgrounds': [
    {'type':'Background',
          'name':'bgBody',
          'title':'Addresses',
          'size':(416, 550),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileSave',
                   'label':'&Save\tCtrl+S',
                   'command':'save',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'Edit',
             'label':'&Edit',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuEditUndo',
                   'label':'&Undo\tCtrl+Z',
                   'command':'editUndo',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditRedo',
                   'label':'&Redo\tCtrl+Y',
                   'command':'editRedo',
                  },
                  {'type':'MenuItem',
                   'name':'editSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditCut',
                   'label':'Cu&t\tCtrl+X',
                   'command':'editCut',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditCopy',
                   'label':'&Copy\tCtrl+C',
                   'command':'editCopy',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditPaste',
                   'label':'&Paste\tCtrl+V',
                   'command':'editPaste',
                  },
                  {'type':'MenuItem',
                   'name':'editSep2',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditFind',
                   'label':'Find...\tCtrl+F',
                   'command':'findRecord',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditFindNext',
                   'label':'Find Next\tF3',
                   'command':'findNextRecord',
                  },
                  {'type':'MenuItem',
                   'name':'editSep3',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditClear',
                   'label':'Cle&ar\tDel',
                   'command':'editClear',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditSelectAll',
                   'label':'Select A&ll\tCtrl+A',
                   'command':'editSelectAll',
                  },
                  {'type':'MenuItem',
                   'name':'editSep4',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditNewCard',
                   'label':'&New Card\tCtrl+N',
                   'command':'editNewCard',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditDeleteCard',
                   'label':'&Delete Card',
                   'command':'editDeleteCard',
                  },
              ]
             },
             {'type':'Menu',
             'name':'Go',
             'label':'&Go',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuGoFirstCard',
                   'label':'&First Card\tCtrl+1',
                   'command':'goFirst',
                  },
                  {'type':'MenuItem',
                   'name':'menuGoPrevCard',
                   'label':'&Prev Card\tCtrl+2',
                   'command':'goPrev',
                  },
                  {'type':'MenuItem',
                   'name':'menuGoNextCard',
                   'label':'&Next Card\tCtrl+3',
                   'command':'goNext',
                  },
                  {'type':'MenuItem',
                   'name':'menuGoLastCard',
                   'label':'&Last Card\tCtrl+4',
                   'command':'goLast',
                  },
                  {'type':'MenuItem',
                   'name':'goSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuGoSort',
                   'label':'&Sort Cards...',
                   'command':'sort',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'StaticBox', 
    'name':'StaticBox1', 
    'position':(285, 120), 
    'size':(120, 150), 
    },

{'type':'TextField', 
    'name':'Name', 
    'position':(100, 10), 
    'size':(241, 24), 
    },

{'type':'TextField', 
    'name':'Company', 
    'position':(100, 40), 
    'size':(241, 23), 
    },

{'type':'TextField', 
    'name':'Street', 
    'position':(100, 70), 
    'size':(241, 23), 
    },

{'type':'TextField', 
    'name':'City', 
    'position':(100, 100), 
    'size':(171, 23), 
    },

{'type':'TextField', 
    'name':'State', 
    'position':(100, 130), 
    'size':(39, 23), 
    },

{'type':'TextField', 
    'name':'Zip', 
    'position':(100, 160), 
    'size':(85, 23), 
    },

{'type':'TextField', 
    'name':'Phone1', 
    'position':(100, 190), 
    'size':(169, -1), 
    },

{'type':'TextField', 
    'name':'Phone2', 
    'position':(100, 220), 
    'size':(169, -1), 
    },

{'type':'TextField', 
    'name':'Phone3', 
    'position':(100, 250), 
    'size':(169, -1), 
    },

{'type':'TextField', 
    'name':'Phone4', 
    'position':(100, 280), 
    'size':(169, -1), 
    },

{'type':'TextField', 
    'name':'Email', 
    'position':(100, 310), 
    'size':(300, -1), 
    },

{'type':'TextField', 
    'name':'Web', 
    'position':(100, 340), 
    'size':(300, -1), 
    },

{'type':'TextArea', 
    'name':'Notes', 
    'position':(100, 370), 
    'size':(300, 135), 
    },

{'type':'StaticText', 
    'name':'NameLabel', 
    'position':(5, 15), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Name', 
    },

{'type':'StaticText', 
    'name':'CompanyLabel', 
    'position':(5, 45), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Company', 
    },

{'type':'StaticText', 
    'name':'StreetLabel', 
    'position':(5, 80), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Street', 
    },

{'type':'StaticText', 
    'name':'CityLabel', 
    'position':(5, 105), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'City', 
    },

{'type':'StaticText', 
    'name':'StateLabel', 
    'position':(5, 135), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'State', 
    },

{'type':'StaticText', 
    'name':'ZipCodeLabel', 
    'position':(5, 165), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Zip Code', 
    },

{'type':'StaticText', 
    'name':'TelephoneLabel', 
    'position':(5, 195), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Telephone', 
    },

{'type':'StaticText', 
    'name':'EmailLabel', 
    'position':(5, 315), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Email', 
    },

{'type':'StaticText', 
    'name':'WebLabel', 
    'position':(5, 345), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Web', 
    },

{'type':'StaticText', 
    'name':'NotesLabel', 
    'position':(5, 375), 
    'size':(68, -1), 
    'alignment':'right', 
    'text':'Notes', 
    },

{'type':'Button', 
    'name':'NewCard', 
    'position':(293, 208), 
    'size':(100, -1), 
    'command':'editNewCard', 
    'label':'New Card', 
    },

{'type':'Button', 
    'name':'DeleteCard', 
    'position':(293, 238), 
    'size':(100, -1), 
    'command':'editDeleteCard', 
    'label':'Delete Card', 
    },

{'type':'Button', 
    'name':'Find', 
    'position':(293, 178), 
    'size':(100, -1), 
    'command':'findRecord', 
    'label':'Find', 
    },

{'type':'ImageButton', 
    'name':'Prev', 
    'position':(309, 136), 
    'size':(26, 30), 
    'border':'transparent', 
    'command':'goPrev', 
    'file':'prev.gif', 
    },

{'type':'ImageButton', 
    'name':'Next', 
    'position':(349, 137), 
    'size':(25, 30), 
    'border':'transparent', 
    'command':'goNext', 
    'file':'next.gif', 
    },

{'type':'TextField', 
    'name':'Sortorder', 
    'position':(0, -5), 
    'size':(30, 19), 
    'text':'1', 
    'visible':False, 
    },

{'type':'TextField', 
    'name':'NameOrder', 
    'position':(141, -5), 
    'size':(73, 19), 
    'text':'last word', 
    'visible':False, 
    },

{'type':'TextField', 
    'name':'CorrectName', 
    'position':(100, -5), 
    'size':(241, 24), 
    'visible':False, 
    },

] # end components
} # end background
] # end backgrounds
} }
