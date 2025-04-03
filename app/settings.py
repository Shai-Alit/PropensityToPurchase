# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:27:07 2025

@author: seford
"""

if os.path.exists('./img'):
    img_loc = './img'
else:
    img_loc = '../img'

if os.path.exists('./models'):
    pickle_path = './models'
else:
    pickle_path = '../models'
