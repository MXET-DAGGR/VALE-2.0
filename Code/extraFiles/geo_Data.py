#Author: Evan Maraist
#Email: emaraist1357@gmail.com
#Team BAST - ESET Capstone Project 2020

from shapely.geometry import Point, Polygon, LineString
#Insure Shapely library is installed

#Points of reference on campus
#Polygons represent No-go areas, lines represent acceptable areas bordering them

#Ross Street
Ross_coords = [(30.616525,-96.343014),(30.619695,-96.338443),(30.619638,-96.338397),(30.616465,-96.342978)]
Ross_St = Polygon(Ross_coords)

#Spence Street
Spence_coords = [(30.618319,-96.338717),(30.618303,-96.338745),(30.621464,-96.341560),(30.621491, -96.341533),
                 (30.620737, -96.340826)]
Spence_St = Polygon(Spence_coords)

#Ross St Sidewalks
#Ross southern sidewalk
Ross_S = LineString([(30.616435,-96.342951), (30.619770,-96.338172)])
#Ross northern sidewalk
Ross_N = LineString([(30.616556, -96.343055),(30.617784, -96.341290),(30.617880, -96.341153),
                     (30.617880, -96.341153),(30.619018, -96.339505),(30.619033, -96.339458),
                     (30.619128, -96.339326),(30.619208, -96.339294),(30.619739, -96.338518)])

#Spence Street Sidewalks
#Spence Northeastern sidewalk
Spence_NE = LineString([(30.618296, -96.338668),(30.618758, -96.339072),(30.618880, -96.339130),(30.619016, -96.339246),(30.619114, -96.339328),
                        (30.619171,-96.339341),(30.619657,-96.339782),(30.619686,-96.339774),(30.620006,-96.340115),(30.620318,-96.340394),
                        (30.620372, -96.340383),(30.621092, -96.341031),(30.621092, -96.341031),(30.621522, -96.341446)])
Spence_SW = LineString([(30.618209, -96.338707),(30.618930, -96.339369),(30.619034, -96.339461),
                        (30.620366, -96.340650),(30.620413, -96.340724),(30.621033, -96.341273),
                        (30.621093, -96.341272),(30.621279, -96.341486),(30.621312, -96.341627)])

#Zach Area Sidewalks
Z1 = LineString([(30.620300, -96.340414),(30.621435, -96.339110)])

#Area between Ireland St and Spence St.
S1 = LineString([(30.618813, -96.342019),(30.619344, -96.341141),(30.619772, -96.340520),(30.620238, -96.340489)])

#Ireland St
Ireland_E = LineString([(30.617880, -96.341150),(30.617880, -96.341150),(30.617995, -96.341183),(30.618737, -96.341914),
                        (30.618791, -96.341984),(30.620071, -96.343185)])

# Dictionary of No-Go zones to be iterated through
# "Polygon" is the Shapely defined Polygon area that defines the NoGo zone
# "Reroute2" is a list of the nearby sidewalks/okay locations for each location
global NoGo
NoGo = {
    'Ross_St': {'Polygon': Ross_St,'Reroute2': [Ross_S, Ross_N]},
    'Spence_St': {'Polygon': Spence_St, 'Reroute2':[Spence_NE]}
    }


#Fermier Entrances
FERM_SE = Point(30.616757, -96.341671)
#Thompson Entrances
THOM_W = Point(30.617135, -96.341749)
THOM_E = Point(30.617697, -96.341186)
#Academic Building Entrances
ACAD_W = Point(30.615577,-96.341081)
ACAD_SE = Point(30.615458, -96.340506)
ACAD_E = Point(30.615876, -96.340607)
#Zachry Entrances
ZEEC_SE = Point(30.620824, -96.339823)
ZEEC_W = Point(30.620904, -96.340858)
#Administration Building Entrances
ADMN_NE = Point(30.618847, -96.336262)
#Evans Library entrance
LIBR_NE = Point(30.617214, -96.338649)
#Memorial Student Center entrances
MSC_NW = Point(30.613161, -96.341049)
MSC_SE = Point(30.611258, -96.341833)

#dictionary to hold all of the programmed destinations
global Destinations
Destinations = {
    'FERM': [FERM_SE],
    'THOM': [THOM_E,THOM_W],
    'ACAD': [ACAD_W,ACAD_SE,ACAD_E],
    'ZEEC': [ZEEC_SE,ZEEC_W],
    'ADMN': [ADMN_NE],
    'LIBR': [LIBR_NE],
    'MSC': [MSC_NW,MSC_SE]
    }

global Paths
Paths = {
#     'Ross_S':       {'Sidewalk': Ross_S, 'Neighbors': [Spence_NE]},
    'Ross_N':       {'Sidewalk': Ross_N, 'Neighbors': [Spence_NE]},
    'Spence_NE':    {'Sidewalk': Spence_NE, 'Neighbors': [Z1, Ross_S, Ross_N]},
    #'Spence_SW':    {'Sidewalk': Spence_SW, 'Neighbors': [S1, Ross_S, Ross_N]},
    'Z1':           {'Sidewalk': Z1, 'Neighbors': [Spence_NE]}, #Sidewalk infront of Zach
    'S1':           {'Sidewalk': S1, 'Neighbors': [Ireland_E, Spence_SW]}, #Sidewalk from Ireland to Spence infront of blocker
    'Ireland_E':    {'Sidewalk': Ireland_E, 'Neighbors': [S1, Ross_S, Ross_N]} #East sidewalk of Ireland St

}

#  find closest point  on a line to a point outside of it
def closestPnt(point, line):
    return line.interpolate(line.project(point))

if __name__ == '__main__':
    pt = Point(30.617276, -96.341869) #example point on road
    #for loc in NoGo.keys():  # Read throuh NoGo zones
    #    # print("Testing: ", loc)
    #    if pt.within(NoGo[loc]['Polygon']) == True:  # if point is within NoGo zone
    #        for neighbor in NoGo[loc]['Reroute2']:
    #            eg_prev = Point(30.617076, -96.341682)  # example previous waypt
    #            #print("Previous Point: ", eg_prev)
    #            near_pnt = closestPnt(eg_prev, neighbor)  # closest point on nearby sidewalk to NoGo point
    #            #print("Near Point:", near_pnt)
    #            line = LineString([eg_prev, near_pnt])  # find distance between corrected point and waypoint before it
    #            print("Current Waypoint: ", eg_prev, "\nNearest Point on Line:",near_pnt)