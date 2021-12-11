#Allen Liu
#this script contains functions for returning a dict object containing route attributes and data, and functions 
#for getting specific values from specific keys in returned data objects
from os import name
from arcgis.gis import GIS  
from arcgis.gis import arcgis
import json

#pass a pair of points "start, stop" , returns a dict object returned by ArcGIS API    
def getRoute(stops):                                                  
    # Connect to the routing service and call it
    api_key = "AAPK90fe9ae08c294a7aad9277b33b90544cvnOd5s9SaQZ_KoIsvNHWkkYFkYOS3dAUXQvcx34TDmfQKGOGAwZ9cQH8DEyQTw1y"
    portal = GIS("https://www.arcgis.com", api_key=api_key)
    route = arcgis.network.RouteLayer(portal.properties.helperServices.route.url, gis=portal)
    result = route.solve(stops=stops, 
                    # enter the travel mode object
                        travel_mode = "walk",
                        start_time="now", 
                        return_directions=True, 
                        directions_language="en")


    #write dict object to file path
    with open('/Users/allenliu/CapstoneCode/TempFiles/result', 'w') as myFile:
        json.dump(result, myFile, indent=4)

    return result


#returns the list of points between start and stop points                                         
def parse_route(results):                                             
    
    route = results["routes"]["features"][0]["geometry"]["paths"]    #get value at key "path"
    extracted_route = []                                            #list containing n elements where each element is a (longitude, latitude) pair

    for x in range(len(route[0])):                                  #creates an n x 2 matrix of coordinates
        extracted_route.append(route[0][x])

    return extracted_route

def switchLatLong(list):
    for x in range(len(list)):
        lat = list[x][1]
        long = list[x][0]
        list[x][0] = lat
        list[x][1] = long
    return list

#return the path between thompson and evans
if __name__ == "__main__":
    stops = " -96.34130230264829, 30.617414376325833; -96.33933580264828, 30.61691821112736"
    results = getRoute(stops)
    print(parse_route(results))




