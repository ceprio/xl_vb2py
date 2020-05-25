"""Make the website"""

import mako.template
import mako.lookup
import glob
import os
from vb2py import utils
from vb2py.utils import TextColours as C

#
# Key paths
ROOT_PATH = utils.relativePath('..', 'website')
MAKO_PATH = os.path.join(ROOT_PATH, 'mako')

if __name__ == '__main__':
    print('Creating website ...')
    mako_files = glob.glob(os.path.join(MAKO_PATH, '*.mako'))
    lookup = mako.lookup.TemplateLookup(directories=[MAKO_PATH])
    for file in mako_files:
        base_name = os.path.splitext(os.path.split(file)[1])[0]
        print('Processing {} ... '.format(base_name), end='')
        template = lookup.get_template('{}.mako'.format(base_name))
        result = template.render()
        with open(os.path.join(ROOT_PATH, '{}.html'.format(base_name)), 'w') as f:
            f.write(result)
        print('{}DONE{}'.format(C.OKBLUE, C.ENDC))
