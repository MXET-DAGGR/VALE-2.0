# Author: Evan Maraist
# Email: emaraist1357@gmail.com
# Team BAST - ESET Capstone Project 2020
import math
from shapely.geometry import Point, LineString
from geo_Data import NoGo, Destinations, Paths
from datetime import datetime
import googlemaps
import L1_gps as gps


gmaps = googlemaps.Client(key='AIzaSyD_8UslXeU3SmCAFmnHzqj4FgdlVAib_z8')


# Insure findDir, geo_Data, GPS, and magnetometer custom files are installed
# Insure Shapely library is installed

class Bearing(object):
    # 'dest' is TAMU defined building name acronym
    # initialization method receives target building acronym and finds its closest entrance
    # init then calls API to get waypts between current location and destination
    def __init__(self, dest):
        gps.connectGPS()

        # Current location in the form of a Shapely point
        myPosition = gps.readPosition()
        print(myPosition)
        self.currentLoc = Point(myPosition[0], myPosition[1])
        #self.currentLoc = Point(30.620544, -96.340131)
        
        self.arrived = False
        # find closest entrance to target building
        lengths = []  # list to hold distances
        for i in Destinations[dest]:
            # create line beginning at current location and ending at a building entrance
            line = LineString([self.currentLoc, i])
            # append length of line to lengths list
            lengths.append(line.length)
        # set target point as the point within dest that is the shortest distance away
        self.target = Destinations[dest][lengths.index(min(lengths))]
        self.getDir(self.currentLoc, self.target)
        self.GMwaypts.append(self.target)  # Make sure our final point is in waypts list, Gmaps leaves it out sometimes
        print("From Google:")
        for i in self.GMwaypts:
            print(i.x, i.y)
        self.mapToSidewalk() #map received points to sidewalks
        print("\nUpdated:")
        for i in self.waypts:
            print("Point: ",i[1].x, i[1].y)
            #print(i)
        print("\n")
        self.currentWaypt_iterator = 0  # to track index number of current waypt
        self.currentWaypt = self.waypts[self.currentWaypt_iterator]
        self.onPath = False #boolean to track if robot is currently navigating to path or not

    # get directions from start to end using Gmaps API, save them in self.waypts
    def getDir(self, start, end):
        # convert Shapely point object into 1x2 array containing lat/long
        self.start_location = [start.x, start.y]
        self.end_location = [end.x, end.y]
        self.GMwaypts = []  # array to store waypoints in Shapely Point form

        now = datetime.now()
        # get directions from Google in the form of a JSON script that is converted to a python list
        whereto = gmaps.directions(self.start_location, self.end_location, mode="walking", departure_time=now)
        # Read through the instruction list and pull out the lat/longs for each waypoints
        for i in whereto[0]['legs'][0]['steps']:  # lists inside dictionaries inside lists inside dictionaries, not exactly, but you get the point
            l1 = []
            # step through list
            # print([i][0]['start_location'])
            l1.append([i][0]['start_location']['lat'])
            l1.append([i][0]['start_location']['lng'])
            # compile waypts into Point object array
            self.GMwaypts.append(Point(l1[0], l1[1]))

    #this does..a lot
    #Read through Gmaps waypoints and map them to sidewalks
    #First point just gets mapped to closest sidewalk
    #All other points get mapped to closest sidewalk that is also closest to previous waypoint
    #If previous point and current point have are on paths that intersect a new point is added between them...
    #...which is at the intersection of the two paths
    def mapToSidewalk(self):
        self.waypts = []# [waypt#][path line, nearest point on path]
        prev_path = None
        for pt in self.GMwaypts: #reads through list of GMaps given points, current point in list is "pt"
            print("Correcting Point: ", pt)
            #if its the first waypoint just map it to closest sidewalk
            if self.GMwaypts.index(pt) == 0:
                path_info = [] #[#][path line, nearest point on path]
                dist_to_path = []
                for path in Paths.keys():
                    #print("Sidewalk Key: ", path)
                    temp_list = []
                    temp_list.append(Paths[path]['Sidewalk']) #add linestring for path
                    temp_list.append(self.closestPnt(pt, temp_list[0])) #add nearest point on that linestring
                    dist_to_path.append(self.currentLoc.distance(temp_list[1])) #distance to that point
                    path_info.append(temp_list) #this is how you make arrays of arrays in python
                self.waypts.append(path_info[dist_to_path.index(min(dist_to_path))]) #add linestring/point for closest linestring
                prev_path = self.waypts[0]
                print("First point corrected.")
            else:
                path_info = []  # [#][path line, nearest point on path]
                dist_to_path = []
                for path in Paths.keys():
                    #print("Sidewalk Key: ", path)
                    temp_list = []
                    temp_list.append(Paths[path]['Sidewalk'])  # add linestring for path
                    temp_list.append(self.closestPnt(pt, temp_list[0]))  # add nearest point on that linestring
                    path_info.append(temp_list) #add to array
                    dist_to_path.append(pt.distance(temp_list[1])) #calculate distance from given pt to path
                nxt_path = path_info[dist_to_path.index(min(dist_to_path))] #select point that was closest to pt
                #if paths intersect, add intersection point first
                if prev_path[0].crosses(nxt_path[0]):
                    intersect_pt = prev_path[0].intersection(nxt_path[0])
                    print("Paths intersected. Intersect Point: ", intersect_pt)
                    intersect_path = [prev_path[0],intersect_pt]
                    self.waypts.append(intersect_path)
                else:
                    print("Paths did not intersect")
                self.waypts.append(nxt_path)
                prev_path = nxt_path


    #checks to see if Vale is within 2m of current sidewalk path
    def nearPath(self):
        if self.currentLoc.distance(self.currentWaypt[0]) < 0.000035:
            return True
        else:
            return False

    #gets current location using onboard GPS
    def getLoc(self):
        myPosition = gps.readPosition()
        self.currentLoc = Point(myPosition[0], myPosition[1])

    # return direction (0-359degrees) to aim at to reach destination
    def getBearing(self):
        # Math to calculate target bearing given two sets of points on earths surface
        A = math.radians(self.currentLoc.x)
        B = math.radians(self.currentLoc.y)
        C = math.radians(self.currentWaypt[1].x)
        D = math.radians(self.currentWaypt[1].y)
        # print(A,B,C,D)
        # complicated math for finding bearing between two points on Earth's surface
        x = math.cos(C) * math.sin(D - B)
        y = math.cos(A) * math.sin(C) - math.sin(A) * math.cos(C) * math.cos(D - B)
        b = math.degrees(math.atan2(x, y))
        bearing = (b + 360) % 360
        if bearing == 360:  # offset calculation only works for 0-359 degrees
            bearing = 0
        return bearing

    #  find distance of the length of the line from point to line
    def pntToLineDist(self, point, line):
        x = point
        y = line
        #  closest point on y to x
        pnt = y.interpolate(y.project(x))
        line = LineString([x, pnt])
        return line.length

    #  find closest point  on a line to a point outside of it
    def closestPnt(self, point, line):
        return line.interpolate(line.project(point))

    #  determine if a point (pnt) is in a NoGo zone
    def isNoGo(self, pnt):
        #  Array of NoGo zones point is within
        y = []
        #  Out of Bounds
        out_of_bounds = False
        for i in NoGo:
            if pnt.within(i):
                y.append(i)
                out_of_bounds = True
        if out_of_bounds:
            return True
        else:
            return False


    # check if current position is within 1m of destination
    # check if Vale is on path
    def checkWaypt(self):
        near = 0.00003 # 0.00003 degrees is equal to 3m
        # check if current location is within 1m
        if self.currentLoc.distance(self.currentWaypt[1]) <= near:
            self.onPath = True
            print("Reached waypoint: ", self.currentWaypt[1])
            # if it is, increment to next waypt
            self.currentWaypt_iterator = self.currentWaypt_iterator + 1
            # if current index exceeds length of direction waypts, you have arrived
            if self.currentWaypt_iterator > (len(self.waypts)-1):
                self.arrived = True
                print("Robot has arrived.")
            else:
                self.currentWaypt = self.waypts[self.currentWaypt_iterator]
                print("Incrementing to next waypoint.")
        else:
            self.checkOnPath()


    #check if we've strayed off of the sidewalk we were navigating on
    #if we have, add nearest point on the sidewalk as our next path
    #if we're trying to get back to the path, don't keep adding more path waypoints
    def checkOnPath(self):
        if self.onPath:
            print("Was on path.")
            if self.nearPath() is False: #if not near current sidewalk path
                print("Went off path. Correcting.")
                new_info = [self.currentWaypt[0], self.closestPnt(self.currentLoc,self.currentWaypt[0])]
                print("Corrected to: ", new_info[1])
                self.waypts.insert(self.currentWaypt_iterator,new_info)
                self.currentWaypt = self.waypts[self.currentWaypt_iterator]
                self.onPath = False
            else:
                print("Still on path.")
        else:
            print("Was off path.")
            if self.nearPath():
                self.onPath = True
                print("Back on path.")
            else:
                print("Still off path.")


# Bearing test functionality
if __name__ == "__main__":
    example = Bearing("LIBR")
    while example.arrived == False:
        x_cord = float(input("Input Current X-coordinate: "))
        y_cord = float(input("Input Current Y-coordinate: "))
        example.currentLoc = Point(x_cord, y_cord)
        example.checkWaypt()
        print("Current Location: ", example.currentLoc)
        print("Current Target: ", example.currentWaypt[1])
        print("Current Bearing: ",example.getBearing())
