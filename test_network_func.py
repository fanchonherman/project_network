#the following lines add the root directory of the project to os.path

import os.path
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + '..')*2)


import network_func


def test_network():
    
    assert 

