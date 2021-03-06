{'type':'CustomDialog',
    'name':'nextVersion',
    'title':'Next Release Version Number',
    'position':(169, 114),
    'size':(260, 145),
    'components': [

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(10, 10), 
    'text':'Please confirm the next release version number:', 
    },

{'type':'Spinner', 
    'name':'majorVersion', 
    'position':(10, 40), 
    'size':(47, -1), 
    'max':100, 
    'min':0, 
    'value':11, 
    },

{'type':'Spinner', 
    'name':'minorVersion', 
    'position':(87, 40), 
    'size':(47, -1), 
    'max':100, 
    'min':0, 
    'value':0, 
    },

{'type':'Spinner', 
    'name':'fixLevel', 
    'position':(164, 40), 
    'size':(47, -1), 
    'max':100, 
    'min':0, 
    'value':0, 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnOK', 
    'position':(10, 90), 
    'default':1, 
    'label':'OK', 
    },

{'type':'Button', 
    'id':5101, 
    'name':'btnCancel', 
    'position':(90, 90), 
    'label':'Cancel', 
    },

] # end components
} # end CustomDialog
