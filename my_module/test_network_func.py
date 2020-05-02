#the following lines add the root directory of the project to os.path

import os.path
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + '..')*2)

import pytest
import matplotlib.pyplot as plt

import network_func

@pytest.mark.mpl_image_compare
def test_type_transport('walk'):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot([1,2,3])
    return fig
    


