{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Kunden Datenbank',
          'size':(502, 467),
         'components': [

{'type':'RadioGroup', 
    'name':'sortBy', 
    'position':(8, 67), 
    'size':(134, -1), 
    'items':['Name', 'Firma'], 
    'label':'Sortiere nach:', 
    'layout':'vertical', 
    'max':1, 
    'stringSelection':'Name', 
    },

{'type':'Button', 
    'name':'delButt', 
    'position':(340, 390), 
    'size':(55, -1), 
    'backgroundColor':(255, 0, 0), 
    'label':'L\xf6schen', 
    },

{'type':'Button', 
    'name':'newButt', 
    'position':(400, 390), 
    'size':(84, -1), 
    'backgroundColor':(0, 128, 0), 
    'label':'Neuer Kunde', 
    },

{'type':'TextField', 
    'name':'selectedFld', 
    'position':(230, 390), 
    'size':(33, -1), 
    'text':'0', 
    },

{'type':'StaticText', 
    'name':'homepageTag', 
    'position':(150, 365), 
    'text':'Homepage:', 
    },

{'type':'StaticText', 
    'name':'telMobiTag', 
    'position':(340, 320), 
    'text':'TelMobi:', 
    },

{'type':'StaticText', 
    'name':'telFaxTag', 
    'position':(340, 345), 
    'text':'TelFax:', 
    },

{'type':'StaticText', 
    'name':'telPrivTag', 
    'position':(150, 340), 
    'text':'TelPriv:', 
    },

{'type':'StaticText', 
    'name':'telBusiTag', 
    'position':(150, 315), 
    'text':'TelBusi:', 
    },

{'type':'StaticText', 
    'name':'titleTag', 
    'position':(350, 90), 
    'text':'Titel:', 
    },

{'type':'StaticText', 
    'name':'functionTag', 
    'position':(150, 90), 
    'text':'Funktion:', 
    },

{'type':'StaticText', 
    'name':'notesTag', 
    'position':(150, 195), 
    'text':'Bemerkung:', 
    },

{'type':'StaticText', 
    'name':'emailTag', 
    'position':(150, 155), 
    'text':'Email:', 
    },

{'type':'StaticText', 
    'name':'companyTag', 
    'position':(150, 175), 
    'text':'Firma:', 
    },

{'type':'StaticText', 
    'name':'ortTag', 
    'position':(150, 130), 
    'text':'Ort:', 
    },

{'type':'StaticText', 
    'name':'streetTag', 
    'position':(150, 110), 
    'size':(35, -1), 
    'text':'Strasse:', 
    },

{'type':'StaticText', 
    'name':'nameTag', 
    'position':(150, 65), 
    'size':(41, 12), 
    'text':'Name:', 
    },

{'type':'TextField', 
    'name':'firstName', 
    'position':(210, 65), 
    'size':(98, -1), 
    },

{'type':'TextField', 
    'name':'name', 
    'position':(310, 65), 
    'size':(172, -1), 
    },

{'type':'TextField', 
    'name':'function', 
    'position':(210, 85), 
    'size':(127, -1), 
    },

{'type':'TextField', 
    'name':'title', 
    'position':(380, 85), 
    'size':(102, -1), 
    },

{'type':'TextField', 
    'name':'street', 
    'position':(210, 105), 
    'size':(272, -1), 
    },

{'type':'TextField', 
    'name':'zipCode', 
    'position':(210, 125), 
    'size':(78, -1), 
    },

{'type':'TextField', 
    'name':'city', 
    'position':(290, 125), 
    'size':(193, -1), 
    },

{'type':'TextField', 
    'name':'email', 
    'position':(210, 150), 
    'size':(273, -1), 
    },

{'type':'TextField', 
    'name':'company', 
    'position':(210, 170), 
    'size':(273, -1), 
    },

{'type':'TextArea', 
    'name':'notes', 
    'position':(210, 190), 
    'size':(271, 131), 
    },

{'type':'TextField', 
    'name':'telBusi', 
    'position':(210, 320), 
    'size':(125, -1), 
    },

{'type':'TextField', 
    'name':'telMobi', 
    'position':(380, 320), 
    },

{'type':'TextField', 
    'name':'telPriv', 
    'position':(210, 340), 
    'size':(125, -1), 
    },

{'type':'TextField', 
    'name':'telFax', 
    'position':(380, 340), 
    },

{'type':'TextField', 
    'name':'homepage', 
    'position':(210, 360), 
    'size':(274, -1), 
    },

{'type':'StaticText', 
    'name':'headline', 
    'position':(5, 10), 
    'size':(476, 31), 
    'alignment':'center', 
    'backgroundColor':(128, 128, 192), 
    'font':{'size': 20, 'faceName': 'Arial', 'style': 'bold', 'family': 'serif'}, 
    'foregroundColor':(0, 0, 125), 
    'text':'Kunden Datenbank', 
    },

{'type':'Button', 
    'name':'nextButt', 
    'position':(265, 390), 
    'size':(19, 23), 
    'font':{'size': 10}, 
    'label':'>', 
    },

{'type':'Button', 
    'name':'prevButt', 
    'position':(210, 390), 
    'size':(20, 23), 
    'font':{'size': 10}, 
    'label':'<', 
    },

{'type':'List', 
    'name':'companyList', 
    'position':(6, 130), 
    'size':(138, 277), 
    'items':[], 
    },

{'type':'TextArea', 
    'name':'editArea', 
    'position':(213, 40), 
    'size':(400, 440), 
    'visible':0, 
    },

{'type':'StaticText', 
    'name':'CompanyListTxt', 
    'position':(5, 50), 
    'size':(73, 17), 
    'text':'Kunden:', 
    },

] # end components
} # end background
] # end backgrounds
} }
