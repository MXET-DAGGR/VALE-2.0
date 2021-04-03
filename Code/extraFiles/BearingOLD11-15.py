#Author: Evan Maraist
#Email: emaraist1357@gmail.com
#Team BAST - ESET Capstone Project 2020
import math
from shapely.geometry import Point, LineString
from geo_Data import NoGo, Destinations
from datetime import datetime
import googlemaps
import L1_gps as gps

gmaps = googlemaps.Client(key='AIzaSyD_8UslXeU3SmCAFmnHzqj4FgdlVAib_z8')

# Insure findDir, geo_Data, GPS, and magnetometer custom files are installed
# Insure Shapely library is installed

class Bearing(object):
    #'dest' is TAMU defined building name acronym
    #initialization method receives target building acronym and finds its closest entrance
    #init then calls API to get waypts between current location and destination
    def __init__(self, dest):
        gps.connectGPS()
        
        #Current location in the form of a Shapely point
        myPosition=gps.readPosition()
        print('My Position: ', myPosition)
        self.currentLoc = Point(myPosition[0], myPosition[1])

        #self.currentLoc = Point(30.617449, -96.341886)
        self.arrived = False
        #find closest entrance to target building
        lengths = [] #list to hold distances
        for i in Destinations[dest]:
            #create line beginning at current location and ending at a building entrance
            line = LineString([self.currentLoc,i])
            #append length of line to lengths list
            lengths.append(line.length)
            #print(line.length)
        #set target point as the point within dest that is the shortest distance away
        #print(lengths.index(min(lengths)))
        self.target = Destinations[dest][lengths.index(min(lengths))]


        self.getDir(self.currentLoc, self.target)
        self.waypts.append(self.target) #Make sure our final point is in waypts list, Gmaps leaves it out sometimes
        self.currentWaypt_iterator = 0   #to track index number of current waypt
        self.currentWaypt = self.waypts[self.currentWaypt_iterator]

        print("From Google:")
        for i in self.waypts:
            print(i.x, i.y)
        #check through received waypts and insure they're not in NoGo zones
        #if they are, reroute them to nearby okay zone
        iterator = 0 #to track which point we're on
        for pt in self.waypts: #check every point received from GoogleMaps
            #print("Checking: ", pt)
            for loc in NoGo.keys(): #Read throuh NoGo zones
                #print("Testing: ", loc)
                if pt.within(NoGo[loc]['Polygon']) == True: #if point is within NoGo zone
                    nearest = [] #to hold nearest points
                    neighbor_lengths = [] # to hold distances to nearest points
                    for neighbor in NoGo[loc]['Reroute2']:
                        print("Neighbor line: ",neighbor)
                        #print("Point was out of bounds.")
                        #map it to the nearest sidewalk
                        near_pnt = self.closestPnt(self.waypts[iterator], neighbor) #closest point on nearby sidewalk to NoGo point
                        #print("Near Point:", near_pnt)
                        nearest.append(near_pnt)
                        line = LineString([self.waypts[iterator-1], near_pnt]) #find distance between corrected point and waypoint before it
                        # append length of line to lengths list
                        neighbor_lengths.append(line.length)
                        #print("Current Waypoint: ",self.waypts[iterator-1], "\tNearest Point on Line:",near_pnt)
                    self.waypts[iterator] = nearest[neighbor_lengths.index(min(neighbor_lengths))]
                    print("Corrected a point.")
            iterator = iterator + 1

        print("\nUpdated:")
        for i in self.waypts:
            print(i.x, i.y)
        print("\n")

    #get directions from start to end using Gmaps API, save them in self.waypts
    def getDir(self, start, end):
        # convert Shapely point object into 1x2 array containing lat/long
        self.start_location = [start.x,start.y]
        self.end_location = [end.x,end.y]
        self.waypts = [] # array to store waypoints in Shapely Point form

        now = datetime.now()
        # get directions from Google in the form of a JSON script that is converted to a python list
        whereto = gmaps.directions(self.start_location, self.end_location, mode="walking", departure_time=now)
        # Read through the instruction list and pull out the lat/longs for each waypoints
        for     i in whereto[0]['legs'][0]['steps']: #lists inside dictionaries inside lists inside dictionaries, not exactly, but you get the point
            l1 = []
            # step through list
            # print([i][0]['start_location'])
            l1.append([i][0]['start_location']['lat'])
            l1.append([i][0]['start_location']['lng'])
            # compile waypts into Point object array
            self.waypts.append(Point(l1[0],l1[1]))

    def getLoc(self):
        myPosition=gps.readPosition()
        self.currentLoc = Point(myPosition[0], myPosition[1])
    # return direction (0-359degrees) to aim at to reach destination
    def getBearing(self):
        # Math to calculate target bearing given two sets of points on earths surface
        A = math.radians(self.currentLoc.x)
        B = math.radians(self.currentLoc.y)
        C = math.radians(self.currentWaypt.x)
        D = math.radians(self.currentWaypt.y)
        # print(A,B,C,D)
        #complicated math for finding bearing between two points on Earth's surface
        x = math.cos(C) * math.sin(D - B)
        y = math.cos(A) * math.sin(C) - math.sin(A) * math.cos(C) * math.cos(D-B)
        b = math.degrees(math.atan2(x,y))
        bearing = (b + 360) % 360
        print('Bearing', bearing)
        if bearing == 360: #offset calculation only works for 0-359 degrees
            bearing = 0
        return bearing

    #  find distance of the length of the line from point to line
    def pntToLineDist(self, point, line):
        x = point
        y = line
        #  closest point on y to x
        pnt = y.interpolate(y.project(x))
        line = LineString([x, pnt])
        print('Interpolate: ', pnt)
        print('Line: ', line)
        return line.length

    #  find closest point  on a line to a point outside of it
    def closestPnt(self, point, line):
        print('Closest point: ', line.interpolate(line.project(point)))
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

    # this function makes the next waypt in the list our current waypt
    def nextWaypt(self):
        if self.currentWaypt_iterator == len(self.waypts) - 1:
            print("You have arrived.")
            return
        self.currentWaypt_iterator = self.currentWaypt_iterator + 1
        self.currentWaypt = self.waypts[self.currentWaypt_iterator]

    # check if current position is within 1m of destination
    def checkWaypt(self):
        # 0.000090 degrees is equal to 1m
        x1 = self.currentWaypt.x - 0.000090
        y1 = self.currentWaypt.y - 0.000090
        x2 = self.currentWaypt.x + 0.000090
        y2 = self.currentWaypt.y + 0.000090
        # check if current location is within 1m
        if x1<=self.currentLoc.x<=x2 and y1<=self.currentLoc.y<=y2:
            # if it is, increment to next waypt
            self.currentWaypt_iterator = self.currentWaypt_iterator + 1
            if self.currentWaypt_iterator > len(self.waypts):
                self.arrived = True
            else:
                self.currentWaypt = self.waypts[self.currentWaypt_iterator]
        # if current index exceeds length of direction waypts, you have arrived


# Bearing test functionality
if __name__ == "__main__":
    You_Are_Here = Point(30.619723, -96.338451)  # entrance to the PIC
    # User wants to go to the MSC
    example = Bearing("ZEEC")
    #for i in range(0,len(example.waypts)):
    #    # get bearing to next waypoint
    #    print("Current location: ", example.currentLoc)
    #    print("Target: ", example.currentWaypt)
    #    print("Bearing: ", example.getBearing(),"\n")
    #    # make current waypoint our new location
    #    example.currentLoc = example.waypts[i]
    #    # manually increment waypts
    #    example.checkWaypt
