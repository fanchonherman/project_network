## importing all necessary packages
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
from matplotlib import animation
from PIL import Image, ImageOps
from math import radians, degrees, cos, sin, sqrt, atan2, asin, pi
import os
from copy import copy
from PIL import Image, ImageOps
import imageio
plt.ioff()


## we will define a class : a point on earth's surface 
## defined by its latitude and longuitude

class Point(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
        

        
def midpoint(A,B): 
    """return the midpoint (a Point object) of two points (Point objects)"""
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
    """Calculate the distance between two points"""
    return ox.utils.great_circle_vec(A.lat, A.lon, B.lat, B.lon)

def bearing(A, B):
    """Calculate the bearing between two points"""
    return ox.geo_utils.get_bearing((A.lat,A.lon), (B.lat,B.lon))




def next_point(A,B,distance):
    '''given a point A, and a point B, returns a point with a given distance from A in the direction of B '''
    
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



def points_generate(G, route, step = 10):
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
    if trans == 'car':
        icon = "icons/car.png"  ## the path to the icon
        icon_size = 0.045  ## control the size of the icon      
        start_angle = 110  ## the start angle that makes the icon looking the right direction in the start
        fig_title = 'Car animation' ## figure title
        image_name = 'car'  ## the name used to store the image in 'temp' folder, exemple : car1, car2, ...
        net_type='drive'  ## network type
    elif trans == 'bike':
        icon = "icons/bike.png"
        icon_size = 0.04
        start_angle = 10
        fig_title = 'Bike animation'
        image_name = 'bike'
        net_type='bike'
    elif trans == 'pedestrian':
        icon = "icons/pedestrian.png"
        icon_size = 0.01
        start_angle = 20
        fig_title = 'Pedestrian animation'
        image_name = 'pedestrian'
        net_type='walk'
    return (icon, icon_size,start_angle, fig_title, image_name, net_type)



plt.ioff()
def images_generate(G, route, transport ):
    """Create a folder named 'temp', and store images into it."""
    
    ## we'll need to define origin_point and destination_point
    origin = ox.geo_utils.geocode('Maison du Lez, Montpellier, France') ## gives a tuple(latitude, longuitude)
    origin_point = Point(origin[0], origin[1])

    destination = ox.geo_utils.geocode('Place Eugène Bataillon, Montpellier, France')## gives a tuple(latitude, longuitude)
    destination_point = Point(destination[0], destination[1]) 
    
    ## generating points
    points = points_generate(G, route, 10)
    
    ## getting setting of the type of transport
    (icon, icon_size, start_angle, fig_title, image_name, net_type) = settings(transport)
    
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
    

    
def animate(transport):
    
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
    
    ## creating the 'temp' folder and generating images into it
    images_generate(G, route, transport)
    
    ## saving current directory path
    start_path = os.getcwd()
    
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

