import L1_Route as route
import log_data as log

#start and stop points are "long,lat; long, lat")
stops = " -96.34130230264829, 30.617414376325833; -96.33933580264828, 30.6169182111273"

log.pointsToExcel(route.switchLatLong(route.parse_route(route.getRoute(stops))), "WalkTest")
print(route.switchLatLong(route.parse_route(route.getRoute(stops))))
