#the following lines add the root directory of the project to os.path

import os.path
import sys
#import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + '..')*2)

import network_montpellier as net

#@pytest.mark.mpl_image_compare
#def test_type_transport('walk'):
#    fig = plt.figure()
#    ax = fig.add_subplot(1,1,1)
#    ax.plot([1,2,3])
#    return fig
    

def test_distance():
    assert net.distance_type_transport('bike') == 4339.373999999999


def test_animation():
    assert np.isclose(net.animation_type_transport, 1.97163)


def test_times():
    assert net.times('bike', net.type_transport) == 72.55561256408691


def test_type_transport():
    assert np.isclose(net.type_transport('drive'),1.59513)

