#Author: Evan Maraist
#Email: emaraist1357@gmail.com
#Team BAST - ESET Capstone Project 2020

from shapely.geometry import Point, Polygon, LineString
#Insure Shapely library is installed

#Points of reference on campus

#Ross Street
Ross_coords = [(30.616525,-96.343014),(30.619695,-96.338443),(30.619638,-96.338397),(30.616465,-96.342978)]
Ross_St = Polygon(Ross_coords)

#Spence Street
Spence_coords = [(30.618319,-96.338717),(30.618303,-96.338745),(30.621464,-96.341560),(30.621491, -96.341533),
                 (30.620737, -96.340826)]
Spence_St = Polygon(Spence_coords)

#Ross St Sidewalks
#Ross southern sidewalk
Ross_S = LineString([(30.616435,-96.342951),(30.616435,-96.342951),(30.617958, -96.340810),
                     (30.618412, -96.340127),(30.618474, -96.340036),(30.618927, -96.339374),
                     (30.619015, -96.339246),(30.619770,-96.338172)])
#Ross northern sidewalk
Ross_N = LineString([(30.616556, -96.343055),(30.617784, -96.341290),(30.617880, -96.341153),
                     (30.617880, -96.341153),(30.619018, -96.339505),(30.619033, -96.339458),
                     (30.619128, -96.339326),(30.619208, -96.339294),(30.619739, -96.338518)])

#Spence Street Sidewalks
#Spence Northeastern sidewalk
Spence_NE = LineString([(30.617972, -96.338393),(30.618296, -96.338668),(30.618758, -96.339072),
                        (30.618880, -96.339130),(30.619016, -96.339246),(30.619114, -96.339328),
                        (30.619151, -96.339351),(30.619393, -96.339579),(30.619524, -96.339717),
                        (30.619657,-96.339782),(30.619686,-96.339774),(30.620006,-96.340115),
                        (30.620318,-96.340394),(30.620372, -96.340383),(30.621092, -96.341031),
                        (30.621092, -96.341031),(30.621522, -96.341446)])
Spence_SW = LineString([(30.618209, -96.338707),(30.618930, -96.339369),(30.619034, -96.339461),
                        (30.620366, -96.340650),(30.620413, -96.340724),(30.621033, -96.341273),
                        (30.621093, -96.341272),(30.621279, -96.341486),(30.621312, -96.341627)])

#Zach Area Sidewalks
Z1 = LineString([(30.620300, -96.340414),(30.621435, -96.339110)])

#Area between Ireland St and Spence St.
S1 = LineString([(30.618813, -96.342019),(30.619344, -96.341141),(30.619772, -96.340520),
                 (30.620217, -96.340491)])

#Ireland St
Ireland_E = LineString([(30.617880, -96.341150),(30.617995, -96.341183),(30.618737, -96.341914),
                        (30.618791, -96.341984),(30.620071, -96.343185)])


#Evans Library Area
Evans_NW = LineString([(30.616508, -96.340516),(30.617364, -96.339328),(30.618031, -96.338371),
                       (30.618413, -96.337805)])
Evans_Front = LineString([(30.617574, -96.339038),(30.616807, -96.338386)])
Lib_Front = LineString([(30.616833, -96.337608),(30.617123, -96.337863),(30.617915, -96.338569)])
THOM_SE1 = LineString([(30.616261, -96.342096),(30.616715, -96.341484),(30.616735, -96.341364),
                      (30.617320, -96.340492)])
THOM_SE2 = LineString([(30.617400, -96.340369),(30.617502, -96.340111),(30.617830, -96.339602)])
H20 = LineString([(30.617797, -96.341075),(30.617675, -96.341033),(30.617568, -96.340839),
                  (30.617537, -96.340656),(30.617408, -96.340490)])
H20_RING = LineString([(30.617311, -96.340505),(30.617271, -96.340433),(30.617289, -96.340366),
                       (30.617354, -96.340334),(30.617406, -96.340351),(30.617446, -96.340422),
                       (30.617416, -96.340499),(30.617370, -96.340527)])
HECC_E = LineString([(30.617306, -96.340381),(30.617223, -96.340333),(30.616845, -96.340013)])
ANTH_SW = LineString([(30.617782, -96.339708),(30.617352, -96.339316)])
STER_SW = LineString([(30.616997, -96.340996),(30.616787, -96.340707),(30.616679, -96.340595),
                      (30.616636, -96.340592),(30.616384, -96.340376)])

#ACAD Plaza Area
SUL_ROSS = LineString([(30.614741, -96.342294),(30.615436, -96.341279)])
ACAD1 = LineString([(30.616068, -96.341547),(30.615070, -96.340638)])
ACAD2 = LineString([(30.615198, -96.341863),(30.615702, -96.341121)])
ACAD3 = LineString([(30.615007, -96.341684),(30.615486, -96.340993)])
ACAD4 = LineString([(30.615733, -96.342367),(30.615646, -96.342100),(30.615547, -96.341395)])
ACAD5 = LineString([(30.615474, -96.341038),(30.615288, -96.340349),(30.615080, -96.339517)])
ACAD6 = LineString([(30.614723, -96.340653),(30.615420, -96.341295),(30.615918, -96.341756),
                    (30.616757, -96.342558)])
SULN = LineString([(30.615645, -96.341185),(30.616108, -96.341204),(30.616432, -96.341472),
                   (30.616607, -96.341662)])
SULS = LineString([(30.614679, -96.341213),(30.615351, -96.341205)])
ACAD_NW = LineString([(30.615593, -96.342230),(30.615917, -96.341754),(30.616331, -96.341088)])
ACAD_NE = LineString([(30.616727, -96.341497),(30.616227, -96.341003),(30.616194, -96.340940),
                      (30.615575, -96.340320),(30.615318, -96.340276)])
ACAD_SE1 = LineString([(30.614796, -96.341481),(30.615379, -96.340630),(30.615889, -96.339837),
                       (30.616252, -96.339258),(30.616776, -96.338496),(30.616796, -96.338368),
                       (30.617274, -96.337650)])
ACAD_SE2 = LineString([(30.614630, -96.341310),(30.615554, -96.339957)])
MIL_WLK = LineString([(30.616902, -96.343446),(30.613776, -96.340489)])
#FERM_SE = LineString([(30.616604, -96.341663),(30.616097, -96.341188)])
FERM_FD = LineString([(30.616781, -96.341694),(30.616642, -96.341562)]) #sidewalk going straight from FERM front entrance
FERM_FDP = LineString([(30.616644, -96.341864),(30.616893, -96.341491)]) #sw parallel to Ferm
THOM_SW = LineString([(30.616707, -96.341333),(30.617237, -96.341849)])



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
    'Ross_S':       {'Sidewalk': Ross_S, 'Neighbors': [Spence_NE]},
    #'Ross_N':       {'Sidewalk': Ross_N, 'Neighbors': [Spence_NE]},
    'Spence_NE':    {'Sidewalk': Spence_NE, 'Neighbors': [Z1, Ross_S, Ross_N]},
    #'Spence_SW':    {'Sidewalk': Spence_SW, 'Neighbors': [S1, Ross_S, Ross_N]},
    'Z1':           {'Sidewalk': Z1, 'Neighbors': [Spence_NE]}, #Sidewalk infront of Zach
    'S1':           {'Sidewalk': S1, 'Neighbors': [Ireland_E, Spence_SW]}, #Sidewalk from Ireland to Spence infront of blocker
    'Ireland_E':    {'Sidewalk': Ireland_E, 'Neighbors': [S1, Ross_S, Ross_N]}, #East sidewalk of Ireland St
    'SUL_ROSS':     {'Sidewalk': SUL_ROSS,'Neighbors': []},
    'ACAD1':        {'Sidewalk': ACAD1,'Neighbors': []},
    'ACAD2':        {'Sidewalk': ACAD2, 'Neighbors': []},
    'ACAD3':        {'Sidewalk': ACAD3, 'Neighbors': []},
    'ACAD4':        {'Sidewalk': ACAD4, 'Neighbors': []},
    'ACAD5':        {'Sidewalk': ACAD5, 'Neighbors': []},
    'ACAD6':        {'Sidewalk': ACAD6, 'Neighbors': []},
    'SULN':         {'Sidewalk': SULN, 'Neighbors': []},
    'SULS':         {'Sidewalk': SULS, 'Neighbors': []},
    'ACAD_NW':      {'Sidewalk': ACAD_NW, 'Neighbors': []},
    'ACAD_NE':      {'Sidewalk': ACAD_NE, 'Neighbors': []},
    'ACAD_SE1':     {'Sidewalk': ACAD_SE1, 'Neighbors': []},
    'ACAD_SE2':     {'Sidewalk': ACAD_SE2, 'Neighbors': []},
    'MIL_WLK':      {'Sidewalk': MIL_WLK, 'Neighbors': []},
    #'FERM_SE':      {'Sidewalk': FERM_SE, 'Neighbors': []},
    'FERM_FD':      {'Sidewalk': FERM_FD, 'Neighbors': []},
    'FERM_FDP':     {'Sidewalk': FERM_FDP, 'Neighbors': []},
    'Evans_NW':     {'Sidewalk': Evans_NW, 'Neighbors': []},
    'Evans_Front':  {'Sidewalk': Evans_Front, 'Neighbors': []},
    'Lib_Front':    {'Sidewalk': Lib_Front, 'Neighbors': []},
    'THOM_SW':      {'Sidewalk': THOM_SW, 'Neighbors': []},
    'THOM_SE1':     {'Sidewalk': THOM_SE1, 'Neighbors': []},
    'THOM_SE2':     {'Sidewalk': THOM_SE2, 'Neighbors': []},
    'H20':          {'Sidewalk': H20, 'Neighbors': []},
    'H20_RING':     {'Sidewalk': H20_RING, 'Neighbors': []},
    'HECC_E':       {'Sidewalk': HECC_E, 'Neighbors': []},
    'ANTH_SW':      {'Sidewalk': ANTH_SW, 'Neighbors': []},
    'STRG_SW':      {'Sidewalk': STER_SW, 'Neighbors': []}
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
