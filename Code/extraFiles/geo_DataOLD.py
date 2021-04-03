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
#Ross southern sidewalk
Ross_S = LineString([(30.616435,-96.342951), (30.619770,-96.338172)])
#Ross northern sidewalk
Ross_N = LineString([(30.616556, -96.343055),(30.617784, -96.341290),(30.617880, -96.341153),
                     (30.617880, -96.341153),(30.619018, -96.339505),(30.619033, -96.339458),
                     (30.619128, -96.339326),(30.619208, -96.339294),(30.619739, -96.338518)])
#Spence Street
Spence_coords = [(30.618319,-96.338717),(30.618303,-96.338745),(30.621464,-96.341560),(30.621491, -96.341533),
                 (30.620737, -96.340826)]
Spence_St = Polygon(Spence_coords)
#Spence Northeastern sidewalk
Spence_NE = LineString([(30.618296, -96.338668),(30.618758, -96.339072),(30.618880, -96.339130),(30.619016, -96.339246),(30.619114, -96.339328),
                        (30.619171,-96.339341),(30.619657,-96.339782),(30.619686,-96.339774),(30.620006,-96.340115),(30.620318,-96.340394),
                        (30.620348,-96.340358),(30.621092, -96.341031),(30.621092, -96.341031),(30.621522, -96.341446)])
#Test point for Ross/Spence
Pnt_on_Spence_and_Ross = Point(30.619022, -96.339357)

# Dictionary of No-Go zones to be iterated through
# "Reroute2" is the nearby sidewalks for each location, method could be created to check all possible
# sidewalks, but that could start getting out of hand once more sidewalks are added
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
home = Point(30.5991, -96.3389)

#dictionary to hold all of the programmed destinations
global Destinations
Destinations = {
    'FERM': [FERM_SE],
    'THOM': [THOM_E,THOM_W],
    'ACAD': [ACAD_W,ACAD_SE,ACAD_E],
    'ZEEC': [ZEEC_SE,ZEEC_W],
    'ADMN': [ADMN_NE],
    'LIBR': [LIBR_NE],
    'MSC': [MSC_NW,MSC_SE],
    'HME': [home]
    }

#  find closest point  on a line to a point outside of it
def closestPnt(point, line):
    return line.interpolate(line.project(point))

if __name__ == '__main__':
    pt = Point(30.617276, -96.341869) #example point on road
    for loc in NoGo.keys():  # Read throuh NoGo zones
        # print("Testing: ", loc)
        if pt.within(NoGo[loc]['Polygon']) == True:  # if point is within NoGo zone
            for neighbor in NoGo[loc]['Reroute2']:
                eg_prev = Point(30.617076, -96.341682)  # example previous waypt
                #print("Previous Point: ", eg_prev)
                near_pnt = closestPnt(eg_prev, neighbor)  # closest point on nearby sidewalk to NoGo point
                #print("Near Point:", near_pnt)
                line = LineString([eg_prev, near_pnt])  # find distance between corrected point and waypoint before it
                print("Current Waypoint: ", eg_prev, "\nNearest Point on Line:",near_pnt)