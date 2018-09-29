'''
Created on 29.9.2018

@author: Jovana
'''


from execute import execute
import os

execute(os.path.split(__file__)[0], 'grammer.tx', 'test.test', True, True)