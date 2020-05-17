import folium
import time
import networkx as nx
import osmnx as ox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from folium import plugins


def type_transport(transport):
    """This function plot the shortest path for different type of transport from La Maison du Lez, Montpellier, France 
    to Place to Eugène Bataillon, Montpellier, France.
    
    Parameters
    ----------
    transport : string, type of transport to choose to plot his path.
    
    Returns
    -------
    a map showing the shortest path.
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


#Or we can devide the function above in two functions
def create_graph(loc, transport_mode, loc_type="address"):
    """This function Create a networkx graph from any location and any 
    transport mode(type) either from an address or a points(coordinates)
    OSM data within some distance of some address.
    
    Parameters
    ----------
    loc : the address to use as the central point around which to construct the graph
    transport_mode : string, type of street network to get.
    loc_type : string, type of localisation to choose 

    Returns
    -------
    networkx multidigraph for the chosen location.
    """ 
    # Transport mode = ‘walk’, ‘bike’, ‘drive’, ‘drive_service’, ‘all’, ‘all_private’, ‘none’
    if loc_type == "address":
        G = ox.graph_from_address(loc, network_type=transport_mode)
    elif loc_type == "points":
        G = ox.graph_from_point(loc, network_type=transport_mode )
    return G


def short_path(graph, origin, destination):  
    """This function plot the shortest path in the graph and calculate his length.
    
    Returns
    -------
    a networkx graph showing the shortest path.
    """  
    origin_node = ox.get_nearest_node(graph, origin)
    destination_node = ox.get_nearest_node(graph, destination)
    route = nx.shortest_path(graph, origin_node, destination_node)
    route_lentgh = nx.shortest_path_length(graph, origin_node, destination_node)
    chemin = ox.plot_graph_route(graph, route)
    return chemin, route_lentgh


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


def geojson_data(transport):  
    """This function create a data frame composed of latitude, longitude of 
    a shortest path's nodes.
    
    Returns
    -------
    pandas.data.frame.
    """ 
    G = ox.graph_from_place('Montpellier, Hérault, France', network_type=transport)  
    origin = ox.geo_utils.geocode('Maison du Lez, Montpellier, France')
    destination= ox.geo_utils.geocode('Place Eugène Bataillon, Montpellier, France')
    origin_node = ox.get_nearest_node(G, origin)
    destination_node = ox.get_nearest_node(G, destination)
    route = nx.shortest_path(G, origin_node, destination_node)
    
    df=pd.DataFrame(ox.node_list_to_coordinate_lines(G, route))
    data=list(map(list, df[0][0:len(df[0])])) 

    lon = [origin[1]] 
    for i in range(len(data)):
        lon.append(data[i][0])
    
    lat = [origin[0]]
    for i in range(len(data)):
        lat.append(data[i][1])

    if transport == 'drive': t= 4 
    elif transport == 'bike': t = 3.5
    elif transport == 'walk': t = 3 
    
    time= list()
    for i in np.arange(1, t*len(lat), t):
        time.append(i)    
        
    time = list(map(int, time))
    l = len(time)
    df=pd.DataFrame({'lon' : lon,
                     'lat' : lat, 'time' : time},columns=['lon','lat','time'])
    new_row = {'lon':destination[1], 'lat':destination[0], 'time':df['time'][l-1]+t}

    df = df.append(new_row, ignore_index=True)
    return(df)


def geojson_visualization(df):
    """This function animate the shortest path using Timestamped GeoJson.
    
    Parameters
    ----------
    df : data.frame, longtitude an latitude for each node in the shortest path.
    
    Returns
    -------
    an interactive map drawing the shortest path.
    """ 
    m = folium.Map(
    location=[43.61032245, 3.8966295],
    tiles="cartodbpositron",
    zoom_start=13)
    
    
    lines = [
        {
            'coordinates': [
                [df.loc[i, 'lon'], df.loc[i, 'lat']],
                [df.loc[i+1, 'lon'], df.loc[i+1, 'lat']],
            ],
            'dates': [
                pd.to_datetime(df.loc[i,'time'], unit='m', origin=pd.Timestamp('2020-05-19')).__str__(),
                pd.to_datetime(df.loc[i+1,'time'], unit='m', origin=pd.Timestamp('2020-05-19')).__str__()
            ],
            'color': 'red'
        }
        for i in range(len(df)-1)
    ]
    
     
    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': line['coordinates'],
            },
            'properties': {
                'times': line['dates'],
                'style': {
                    'color': line['color'],
                    'weight': 4  
                },
                'icon': 'circle',
                'iconstyle':{'radius' : 1}
                #                 'iconUrl': "https://www.google.fr/imgres?imgurl=https%3A%2F%2Fstatic.thenounproject.com%2Fpng%2F13133-200.png&imgrefurl=https%3A%2F%2Fthenounproject.com%2Fterm%2Fpedestrian%2F162693%2F&tbnid=Ih-71qXZVedo9M&vet=12ahUKEwiP0vvAkK7pAhUXMRoKHbSzD7oQMygAegUIARDlAQ..i&docid=MBEwWPNEKbzbsM&w=200&h=200&q=icon%20pedestrian&ved=2ahUKEwiP0vvAkK7pAhUXMRoKHbSzD7oQMygAegUIARDlAQ",
                #                 'iconSize': [16, 16]},
                #             'popupTemplate' : "<strong>{pedestrian}</strong>"
            }
        }
        for line in lines
    ]
    
    plugins.TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features,
        }, 
        period='PT1H',
        #     duration = 'PT1M',
        add_last_point=True).add_to(m)


    m.save('geojson_visualization.html')
    return m


def GeoJson_times(parameter, function):
    """This function calculates the time that the given function takes to compile according to the type of transport chosen.

    Parameters
    ----------
    parameter : string or data frame, type of transport of GeoJson data.
    function : the function you want to use.

    Returns
    -------
    the time in seconds that the function took to compile according to the type of transport.
    """
    start = time.time()
    graphe = function(parameter)
    end = time.time()
    temps = end - start
    return(temps)