
{ 'application':{ 'type':'Application',
            'name':'SlideShow',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgSlideShow',
    'title':'slideshow PythonCard Application',
    'size':( 310, 300 ),
    'style':['resizeable'],
    'visible':0,

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'&File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileOpenSlide',
                  'label':'&Open Current Slide\tCtrl+O' },
                { 'type':'MenuItem', 'name':'fileSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] },
            { 'type':'Menu',
              'name':'menuImage',
              'label':'&Slideshow',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuSlideshowChooseDirectory',
                  'label':'Choose &Directory...\tCtrl+D',
                  },
                { 'type':'MenuItem',
                  'name':'menuSlideshowChooseZip',
                  'label':'Choose &Zip...\tCtrl+Z',
                  },
                { 'type':'MenuItem',
                  'name':'menuSlideshowSetInterval',
                  'label':'Set delay &interval...\tCtrl+I',
                  },
                { 'type':'MenuItem',
                  'name':'menuSlideshowShowSlides',
                  'label':'&Show Slides\tCtrl+S',
                  },
                { 'type':'MenuItem',
                  'name':'menuSlideshowContinue',
                  'label':'&Pause/Continue\tF8',
                  },
                { 'type':'MenuItem',
                  'name':'menuSlideshowLoop',
                  'label':'&Loop Slides\tCtrl+L',
                  'checkable':1,
                  'checked':0},
                { 'type':'MenuItem',
                  'name':'menuSlideshowToggleFullScreen',
                  'label':'&Toggle Full Screen\tCtrl+F',
                  'checkable':1,
                  'checked':0},
                { 'type':'MenuItem',
                  'name':'menuSlideshowStopSlides',
                  'label':'Stop Slides\tESC'},
                  {'type':'MenuItem',
                   'name':'menuSlideShowSep1',
                   'label':'-'},
                { 'type':'MenuItem',
                  'name':'menuSlideshowFirstSlide',
                  'label':'First Slide'},
                { 'type':'MenuItem',
                  'name':'menuSlideshowPreviousSlide',
                  'label':'Previous Slide'},
                { 'type':'MenuItem',
                  'name':'menuSlideshowNextSlide',
                  'label':'Next Slide'},
                { 'type':'MenuItem',
                  'name':'menuSlideshowLastSlide',
                  'label':'Last Slide'},
                { 'type':'MenuItem',
                  'name':'menuSlideshowGotoSlide',
                  'label':'&Goto Slide...\tCtrl+G'},
            ] },
            { 'type':'Menu',
              'name':'menuOptions',
              'label':'&Options',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuOptionsIncludeSubDirectories',
                  'label':'&Include Sub-directories',
                  'checkable':1,
                  'checked':0,
                  },
                ] },
        ]
    },

   'components':
   [ 
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 0),
      'size':(150, 150) },
    { 'type':'HtmlWindow',
      'name':'htmlView',
      'position':(0, 0),
      'size':(150, 150),
      'visible':0 },
   ]
  }
 ]
 }
 }

