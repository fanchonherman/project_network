#the following lines add the root directory of the project to os.path

import os.path
import sys
import pytest
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + (os.path.sep + '..')*2)
import network_montpellier as net




def test_distance():
    np.isclose(net.distance_type_transport('bike'), 4339.374)

    

@check_figures_equal()
def test_graph(fig_test, fig_ref):
     fig_test.net.create_graph('Montpellier, France', 'walk', loc_type="address")
     fig_ref.ox.graph_from_address('Montpellier, France', network_type='walk') 
    



def test_short_path_length():
    G = ox.graph_from_place('Montpellier, France', network_type='drive')
    origin = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    destination = ox.geo_utils.geocode('Place Eugène Bataillon, Montpellier, France')
    assert net.short_path(G, origin, destination)[1] == 55



