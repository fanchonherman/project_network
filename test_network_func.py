# the following lines add the root directory of the project to os.path

import os.path
import sys
import network_func

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                (os.path.sep + '..')*2)


# def test_network():
#   assert