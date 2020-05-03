import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def type_transport(transport):
    """This function plot on interactive map of the shortest path for different type of transport from Maison du Lez, Montpellier, France 
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
    fig, ax = ox.plot_graph_route(G, route, origin_point=origin_point, destination_point=destination_point)
    plt.show
    return()

def animation_type_transport(transport):
    """a faire la doc
    """
    G = ox.graph_from_place(
        'Montpellier, Hérault, France', network_type=transport)
    origin_point = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    origin_node = ox.get_nearest_node(G, origin_point)
    destination_point = ox.geo_utils.geocode(
        'Place Eugène Bataillon, Montpellier, France')
    destination_node = ox.get_nearest_node(G, destination_point)
    route = nx.shortest_path(G, origin_node, destination_node)

    fig, ax = ox.plot_graph_route(G, [origin_node])
    pic = ax.scatter(G.nodes[route[0]]['x'], G.nodes[route[0]]['y'], s=50, marker='*',
                     c='b', alpha=1, zorder=6)
    lc = LineCollection([], colors='r', linewidths=4, alpha=0.2, zorder=3)
    ax.add_collection(lc)

    def animate(i):
        pic.set_offsets([G.nodes[route[i+1]]['x'], G.nodes[route[i+1]]['y']])
        lines = ox.node_list_to_coordinate_lines(G, route[:i+1], True)
        lc.set_segments(lines)
        return pic, lc

    ani = animation.FuncAnimation(
        fig, animate, frames=200, interval=100, blit=True, repeat=False)
    plt.show()
    return(ani)
