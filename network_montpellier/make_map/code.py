import networkx as nx
import osmnx as ox
import time
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def type_transport(transport):
    """This function plot on interactive map of the shortest path for different type of transport from La Maison du Lez, Montpellier, France 
    to Place to Eugène Bataillon, Montpellier, France.
    
    Parameters
    ----------
    transport : string, type of transport to choose to plot his path.
    
    Returns
    -------
    an interactive map showing the shortest path.
    """ 
    # download the map as a graph object 
    G = ox.graph_from_place(
        'Montpellier, Hérault, France', network_type=transport)
    # define origin and desination locations 
    origin_point = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    destination_point = ox.geo_utils.geocode(
        'Place Eugène Bataillon, Montpellier, France')
    # get the nearest nodes to the locations 
    origin_node = ox.get_nearest_node(G, origin_point)
    destination_node = ox.get_nearest_node(G, destination_point)
    # finding the shortest path
    route = nx.shortest_path(G, origin_node, destination_node)
    # plot the map graph
    fig, ax = ox.plot_graph_route(G, route, origin_point=origin_point, destination_point=destination_point, route_linewidth=2)
    plt.show
    return()


def distance_type_transport(transport):
    """This function calculates the distance between La Maison du Lez, Montpellier, France and Place 
    to Eugène Bataillon, Montpellier, France in meters.

    Parameters
    ----------
    transport : string, type of transport to choose to calculate the distance.

    Returns
    -------
    the distance between these two places according to the type of transport.
    """
    G = ox.graph_from_place(
        'Montpellier, Hérault, France', network_type=transport)
    origin_point = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    destination_point = ox.geo_utils.geocode(
        'Place Eugène Bataillon, Montpellier, France')
    origin_node = ox.get_nearest_node(G, origin_point)
    destination_node = ox.get_nearest_node(G, destination_point)
    distance = nx.shortest_path_length(
        G, origin_node, destination_node, weight='length')
    return(distance)


def times(transport, function):
    """This function calculates the time that the given function takes to compile according to the type of transport chosen.

    Parameters
    ----------
    transport : string, type of transport.
    function : the function you want to use.

    Returns
    -------
    the time in seconds that the function took to compile according to the type of transport.
    """
    start = time.time()
    graphe = function(transport)
    end = time.time()
    temps = end - start
    return(temps)


def animation_type_transport(transport):
    """This function makes it possible to make an animation; plot the shortest route for different types of transport between 
    La maison du Lez, Montpellier, France and Place Eugène Bataillon, Montpellier, France.

    Parameters
    ----------
    transport : string, type of transport choose to animate his path.

    Returns
    ----------
    an animation that draws the shortest path.
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


class network:
    def __init__(self, transport):
        self.transport = transport

    def distance(self):
        G = ox.graph_from_place(
            'Montpellier, Hérault, France', network_type=self.transport)
        origin_point = ox.geo_utils.geocode(
            'Maison du Lez, Montpellier, France')
        destination_point = ox.geo_utils.geocode(
            'Place Eugène Bataillon, Montpellier, France')
        origin_node = ox.get_nearest_node(G, origin_point)
        destination_node = ox.get_nearest_node(G, destination_point)
        distance = nx.shortest_path_length(
            G, origin_node, destination_node, weight='length')
        return(distance)

