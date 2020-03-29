import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def type_transport(transport):
    """This function plot on interactive map of the shortest path for different type of transport from maison du Lez, Montpellier 
    to Place to Eugène Bataillon, Montpellier, France.
    
    Parameters
    ----------
    transport : type of transport to choose to plot his path
    
     Returns
    -------
    an interactive map showing the shortest path
    """ 
    G = ox.graph_from_place(
        'Montpellier, Hérault, France', network_type=transport)
    origin_point = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    destination_point = ox.geo_utils.geocode(
        'Place Eugène Bataillon, Montpellier, France')
    origin_node = ox.get_nearest_node(G, origin_point)
    destination_node = ox.get_nearest_node(G, destination_point)
    route = nx.shortest_path(G, origin_node, destination_node)
    return(ox.plot_route_folium(G, route, route_width=2, route_color='hotpink'))