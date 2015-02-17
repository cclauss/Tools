# -*- coding: utf-8 -*-
"""
Overwrite a file with zeroes and delete it.
"""

__version__ = '0.0'
__author__ = '671620616'
__created_on__ = 'Wed Dec 31 13:39:26 2014'

import easygui as eg
import os

try:
    f = eg.fileopenbox(msg='Select a file',
                       title='Delete')
    if f == '.':
        raise SystemExit('No file supplied, exiting.')
    opts = eg.multenterbox(msg='Overwrite options',
                           title='Overwrite',
                           fields=['Num. overwrites', 'Overwrite factor'],
                           values=[5, 2])
    overwrites = int(opts[0])
    upscale = int(opts[1])

    with open(f, 'r') as fr:
        fl = len(fr.read())
    # fr.close()  # close() is done automatically at the end the 'with open()' statement

    with open(f, 'w') as fw:
        for i in xrange(overwrites):
            writing = unichr(0) * (fl*upscale)
            fw.write(writing)
    #fw.close()  # close() is done automatically at the end the 'with open()' statement

    os.remove(f)

    errd = False
except:
    eg.exceptionbox()
    errd = True
finally:
    if not errd:
        eg.msgbox(msg='Deleted {} successfully.'.format(f),
                  title='Success')
