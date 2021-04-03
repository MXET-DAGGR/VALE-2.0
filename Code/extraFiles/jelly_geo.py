from shapely.geometry import Point, Polygon, LineString
#Insure Shapely library is installed

#Points of reference on campus
#Polygons represent No-go areas, lines represent acceptable areas bordering them

#Ross Street
Ross_coords = [(30.616525,-96.343014),(30.619695,-96.338443),(30.619638,-96.338397),(30.616465,-96.342978)]
Ross_St = Polygon(Ross_coords)
#Ross southern sidewalk
Ross_S = LineString([(30.616435,-96.342951), (30.619770,-96.338172)])
#Spence Street
Spence_coords = [(30.618319,-96.338717),(30.618303,-96.338742),(30.620197,-96.340413),(30.620213,-96.340383)]
Spence_St = Polygon(Spence_coords)
#Spence Northeastern sidewalk
Spence_NE = LineString([(30.618296, -96.338668),(30.618758, -96.339072),(30.618880, -96.339130),(30.619016, -96.339246),(30.619114, -96.339328),
                        (30.619171,-96.339341),(30.619657,-96.339782),(30.619686,-96.339774),(30.620006,-96.340115),(30.620318,-96.340394),
                        (30.620348,-96.340358),(30.621092, -96.341031),(30.621092, -96.341031),(30.621522, -96.341446)])
#Test point for Ross/Spence
Pnt_on_Spence_and_Ross = Point(30.619022, -96.339357)

#Dictionary of No-Go zones to be iterated through
NoGo = {
    'Ross_St': {'Polygon': Ross_St,'Reroute2':Ross_S},
    'Spence_St': {'Polygon': Spence_St, 'Reroute2':Spence_NE}
    }

#Fermier Entrances
FERM_SE = Point(30.616757, -96.341671)
#Thompson Entrances
THOM_W = Point(30.617135, -96.341749)
THOM_E = Point(30.617697, -96.341186)
#Academic Building Entrances
ACAD_W = Point(30.617697, -96.341186)
ACAD_SE = Point(30.615458, -96.340506)
ACAD_E = Point(30.615876, -96.340607)
#Zachry Entrances
ZEEC_SE = Point(30.615876, -96.340607)
ZEEC_W = Point(30.620904, -96.340858)
#Administration Building Entrances
ADMN_NE = Point(30.618847, -96.336262)
#Evans Library entrance
LIBR_NE = Point(30.617214, -96.338649)
#Memorial Student Center entrances
MSC_NW = Point(30.613161, -96.341049)
MSC_SE = Point(30.611258, -96.341833)

TST = Point(30.440320, -98.006798)


#dictionary to hold all of the programmed destinations
Destinations = {
    'FERM': [FERM_SE],
    'THOM': [THOM_E,THOM_W],
    'ACAD': [ACAD_W,ACAD_SE,ACAD_E],
    'ZEEC': [ZEEC_SE,ZEEC_W],
    'ADMN': [ADMN_NE],
    'LIBR': [LIBR_NE],
    'MSC': [MSC_NW,MSC_SE],
    'TST': [TST]
    }

