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

import matplotlib.image as image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
from matplotlib import animation
from PIL import Image, ImageOps
from math import radians, degrees, cos, sin, sqrt, atan2, asin, pi
import os
from copy import copy
from PIL import Image, ImageOps
import imageio
plt.ioff()


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


#### animation by storing images


class Point(object):
    """a point on earth's surface defined by its latitude and longuitude"""
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
        
        
        
def midpoint(A,B): 
    """return the midpoint (a Point object) of two points (Point objects)
    
    Parameters
    ----------
    A : Point, the first point
    B : Point, the second point
    
    Returns
    -------
    Point, the midpoint between the two given points"""
    ## convert degrees to radians
    lat1, lon1 = radians(A.lat), radians(A.lon)
    lat2, lon2 = radians(B.lat), radians(B.lon)
    
    dLon = lon2-lon1

    Bx = cos(lat2) * cos(dLon)
    By = cos(lat2) * sin(dLon)
    
    ## applying the midpoint formula
    lat3 = atan2(sin(lat1)+sin(lat2), sqrt((cos(lat1)+Bx)*(cos(lat1)+Bx) + By*By))
    lon3 = lon1 + atan2(By, cos(lat1) + Bx)
    return Point(degrees(lat3),degrees(lon3))




def distance(A,B): 
    """Calculate the distance between two points
    
    Parameters
    ----------
    A : Point, the first point
    B : Point, the second point
    
    Returns
    -------
    the distance between the two given points"""
    return ox.utils.great_circle_vec(A.lat, A.lon, B.lat, B.lon)

def bearing(A, B):
    """Calculate the bearing between two points
    
    Parameters
    ----------
    A : Point, the first point
    B : Point, the second point
    
    Returns
    -------
    The bearing of the first point from the second one"""
    return ox.geo_utils.get_bearing((A.lat,A.lon), (B.lat,B.lon))




def next_point(A,B,distance):
    '''given a point A, and a point B, returns a point with a given distance from A in the direction of B 
    
    Parameters
    ----------
    A : Point, the first point
    B : Point, the second point
    distance : int,  
    
    Returns
    -------
    Point, a point that is a given distance (distance) away from the first point, in the direction of the second one '''
    
    ## Radius of the Earth in km
    R = 6378.1 
    
    ## Bearing is degrees converted to radians.
    bear = radians(bearing(A,B)) 
    
    ## Distance in m converted to km
    d = distance/1000 
    
    ## convert degrees to radians
    lat1 = radians(A.lat) 
    lon1 = radians(A.lon) 
    
    ## applying the formula
    lat2 = asin( sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(bear) )
    lon2 = lon1 + atan2(sin(bear) * sin(d/R)* cos(lat1), cos(d/R)- sin(lat1)* sin(lat2))

    #convert back to degrees
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    return Point(lat2, lon2)




def points_generate(G, route, step = 20):
    """returnes a list of points that belong to the same path (route), of the graph G,
    with almost equal distance (step) between each tow points"""
    
    ## this function Given a list of nodes, return a list of lines that together follow the path defined by the list of nodes.
    ## we'll aply it on our route
    lines = ox.plot.node_list_to_coordinate_lines(G, route)
    
    ## creating an empty list
    ll =[]
    
    ## appending the elements of lines
    ## each element is a list of tuples
    for i in lines:
        for j in i:
            ll.append(j)
    ## first point : origin point
    list1 = []
    
    ## for each tuple in each list we append the tuple as a point
    for i in ll:
        list1.append(Point(i[1], i[0]))
    
    ## list2's first element = list1's
    list2 = [list1[0]]
    
    
    rep = list1[0]
    
    ## we remove the points that are too close to each other
    ## as thay are not perfectly aligned
    for i in range(len(list1)-1) :
        
        ## only append if the next point is 50m or more away from current one 
        if distance(rep, list1[i])>50:
            list2.append(list1[i])
            rep = list1[i]
    
    ## points' first element is list2's first one
    points = [list2[0]]
    
    ## between each two points, creat points perfectly aligned with equal distance between them
    ## this will make the animation more uniform
    for i in range(len(list2)-1) :
        if distance(list2[i],list2[i+1])>step:
            for j in np.arange(step, int(distance(list2[i],list2[i+1])), step):
                points.append(next_point(list2[i],list2[i+1], j))
            points.append(list2[i+1])    
        else:
            points.append(list2[i+1])
    return points



def settings(trans):
    """ returns settings for each type of transport"""
    ## getting path to the main directory
    tmp = os.path.abspath(os.path.join(os.getcwd(), '..'))
    if trans == 'car':
        icon = os.path.join(tmp, 'icons', 'car.png')  ## the path to the icon
        icon_size = 0.045  ## control the size of the icon      
        start_angle = 110  ## the start angle that makes the icon looking the right direction in the start
        fig_title = 'Car animation' ## figure title
        image_name = 'car'  ## the name used to store the image in 'temp' folder, exemple : car1, car2, ...
        net_type='drive'  ## network type
    elif trans == 'bike':
        icon = os.path.join(tmp, 'icons', 'bike.png')
        icon_size = 0.04
        start_angle = 10
        fig_title = 'Bike animation'
        image_name = 'bike'
        net_type='bike'
    elif trans == 'pedestrian':
        icon = os.path.join(tmp, 'icons', 'pedestrian.png')
        icon_size = 0.01
        start_angle = 20
        fig_title = 'Pedestrian animation'
        image_name = 'pedestrian'
        net_type='walk'
    return (icon, icon_size,start_angle, fig_title, image_name, net_type)




def images_generate(transport ):
    """Create a folder named 'temp', and store images into it."""
    
    ## to avoid displaying figures while saving them
    plt.ioff()
    
    ## getting setting of the type of transport
    (icon, icon_size, start_angle, fig_title, image_name, net_type) = settings(transport)
    
    origin = ox.geo_utils.geocode('Maison du Lez, Montpellier, France') ## gives a tuple(latitude, longuitude)
    ## we transforme the tuple of coordinates into a point
    origin_point = Point(origin[0], origin[1])

    destination = ox.geo_utils.geocode('Place Eugène Bataillon, Montpellier, France')## gives a tuple(latitude, longuitude)
    ## we transforme the tuple of coordinates into a point
    destination_point = Point(destination[0], destination[1]) 

    ## creatin the midpoint of origin and destination points
    center = midpoint(origin_point, destination_point)
    ##creating the graph from the midpoint
    G = ox.graph_from_point((center.lat, center.lon), network_type=net_type, distance=2000)

    ## nearest nodes
    origin_node = ox.get_nearest_node(G, origin)
    destination_node = ox.get_nearest_node(G, destination)

    ## shortest path
    route = nx.shortest_path(G, origin_node, destination_node)

    ## generating points
    points = points_generate(G, route, 10)
    
    
    ## icon opening (car, bike or pedestrian)
    im1  = Image.open(icon)
    
    ## in pedestrian case, we use mirroring in order to give 
    ## in order to give the impression that the pedestrian is walking
    if transport == 'pedestrian':
        im2 = ImageOps.mirror(im1)
    ## if not pedestrian, im2 will be just im1
    else:
        im2 = im1
    
    ## putting icon in track 
    im1 = im1.rotate(start_angle)
    im2 = im2.rotate(start_angle)
    
    ## saving current directory path
    start_path = os.getcwd()
    ## getting path to the main directory
    tmp = os.path.abspath(os.path.join(os.getcwd(), '..'))
    os.chdir(tmp)
    ## creating path for the folder 'temp' 
    path =os.path.join(os.getcwd(), 'temp')
    
    ## if 'temp' folder already exists, changing directory into it (in order to stor images)
    if 'temp' in os.listdir():
        os.chdir(path)
    ## if not, creating 'temp' folder and changing directory into it
    else:    
        os.mkdir('temp')
        os.chdir(path)
    
    ## for each point in the rode (route)
    for i in range(1,len(points)-1) :
        
        ## creating a ox graph figure
        fig, ax = ox.plot_graph_route(G, route, show=False, close=False)
        ## title
        plt.title(fig_title)
        
        ## controling the icon rotation, in order to have the rotation effect in our animation
        im1 = im1.rotate(bearing(points[i-1], points[i]) + 180 - bearing(points[i+1], points[i]))
        im2 = im2.rotate(bearing(points[i-1], points[i]) + 180 - bearing(points[i+1], points[i]))
        
        ## every five points, replace the im1 by im2
        ## if pedestrian, im2 will be the mirrored im1,
        ## this way the pedestrian looks walking
        if i % 5 ==0:
            tmp = im1
            im1 = im2
            im2 = tmp
            
        ## storing the icon_image in the container 
        img = OffsetImage(im1, zoom=icon_size)
        
        ## creating the artist
        art = AnnotationBbox(img, (points[i].lon, points[i].lat), frameon = False)
        
        ## copy the art container in orther to avoid an error
        new_ab=copy(art)
        
        ## adding the artist
        ax.add_artist(new_ab)
        
        ## storing the text in the container
        offsetbox1 = TextArea("Maison du Lez", minimumdescent=False)
        
        ## creating the artist
        ab = AnnotationBbox(offsetbox1, (origin_point.lon, origin_point.lat),
                            xybox=(-30, -30),
                            xycoords='data',
                            boxcoords="offset points",
                            arrowprops=dict(arrowstyle="->"))
        ## adding the artist
        ax.add_artist(ab)

        ## storing the text in the container
        offsetbox2 = TextArea("Place Eugène Bataillon", minimumdescent=False)
        
        ## creating the artist
        ab = AnnotationBbox(offsetbox2, (destination_point.lon, destination_point.lat),
                            xybox=(30, 30),
                            xycoords='data',
                            boxcoords="offset points",
                            arrowprops=dict(arrowstyle="->"))
        ## adding the artist
        ax.add_artist(ab)
        
        ## saving the fig as a png image
        plt.savefig(image_name+str(i)+'.png')
        
        ## closing the fig
        plt.close('all')
        
    ## returning to start directory
    os.chdir(start_path)
    

    
    
def animate(transport, create_images = False):
    """create animation of a pedestrian, a car, or a a bike, eather by creating, on the fly, a folder named "temp" 
    and storing images into it, or by already existing images """
    
    ## to avoid displaying figures while saving them
    plt.ioff()
    
    ## getting setting of the type of transport
    (icon, icon_size, start_angle, fig_title, image_name, net_type) = settings(transport)
    
    ## Creating the graph for animation
    origin = ox.geo_utils.geocode('Maison du Lez, Montpellier, France') ## gives a tuple(latitude, longuitude)
    ## we transforme the tuple of coordinates into a point
    origin_point = Point(origin[0], origin[1])

    destination = ox.geo_utils.geocode('Place Eugène Bataillon, Montpellier, France')## gives a tuple(latitude, longuitude)
    ## we transforme the tuple of coordinates into a point
    destination_point = Point(destination[0], destination[1]) 

    ## creatin the midpoint of origin and destination points
    center = midpoint(origin_point, destination_point)
    ##creating the graph from the midpoint
    G = ox.graph_from_point((center.lat, center.lon), network_type = net_type, distance=2000)

    ## nearest nodes
    origin_node = ox.get_nearest_node(G, origin)
    destination_node = ox.get_nearest_node(G, destination)

    ## shortest path
    route = nx.shortest_path(G, origin_node, destination_node)
    
    ## if we want to generate images on the fly with this function
    ## creating the 'temp' folder and generating images into it
    if create_images:
        images_generate(G, route, transport)
    
    ## saving current directory path
    start_path = os.getcwd()
    
    ## getting path to the main directory
    tmp = os.path.abspath(os.path.join(os.getcwd(), '..'))
    os.chdir(tmp)
    
    ## changing directory, getting to 'temp' folder
    path =os.path.join(os.getcwd(), 'temp')
    os.chdir(path)
    
    ## creating list to stor images from 'temp' folder
    imagelist = []
    
    ## storing image by image
    for i in range(1, len(points)-1):
        imagelist.append(imageio.imread(image_name + str(i) + '.png'))

    ## creating figure
    fig = plt.figure(figsize=(9, 9)) 
    ## without axis
    plt.axis('off')

    # making axesimage object
    im = plt.imshow(imagelist[0], cmap=plt.get_cmap('jet'), vmin=0, vmax=255) ## vmin and vmax get the color map correct

    # function to update figure
    def updatefig(j):
        # set the data in the axesimage object
        im.set_array(imagelist[j])
        # return the artists set
        return [im]
    
    # starting animation
    anim = animation.FuncAnimation(fig, updatefig, frames=range(537), 
                                  interval=50, blit=True)
    plt.show()
    
    ## returning to start directory
    os.chdir(start_path)
    
    return anim