{'application':{'type':'Application',
          'name':'dbFits',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'dbFits - catalogo fits header',
          'size':(400, 220),

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
         ]
     },
         'components': [

{'type':'StaticText', 
    'name':'cartelleText',
    'position':(10, 50),
    'backgroundColor':(247, 245, 242), 
    'text':'cartelle',
    },

{'type':'StaticText', 
    'name':'dbText',
    'position':(10, 100),
    'backgroundColor':(247, 245, 242), 
    'text':'StaticText2',
    'text':'database'
    },

{'type':'TextField', 
    'name':'db', 
    'position':(10, 120),
    'size':(145, -1), 
    },

{'type':'TextField', 
    'name':'cartelle', 
    'position':(10, 70),
    'size':(145, -1), 
    },

{'type':'Button', 
    'name':'upBtn', 
    'position':(10, 10), 
    'size':(145, -1), 
    'label':'Aggiorna il db', 
    },

{'type':'Button',
    'name':'upDateBtn',
    'position':(200, 10),
    'size':(145, -1),
    'label':'Correggi le date',
    },

{'type':'Button', 
    'name':'resetBtn', 
    'position':(200, 70),
    'size':(145, -1), 
    'label':'Reset', 
    },

{'type':'Button', 
    'name':'save', 
    'position':(200, 120),
    'size':(145, -1), 
    'label':'Salva', 
    },

{'type':'StaticText',
    'name':'message', 
    'position':(10, 150),
    'size':(350, -1),
    'backgroundColor':(247, 245, 242),
    'alignment':'center', 
    'editable':False,
    'text':''
    },

] # end components
} # end background
] # end backgrounds
} }
