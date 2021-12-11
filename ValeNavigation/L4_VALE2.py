import L3_RoverCommand as rover
import time 
import atexit
import L1_Route as route
import VALESpeechRecognition.Speech_Recognition as speech
from VehicleCommand.VALESpeechRecognition.Speech_Recognition import check_bldg, user_input

global destination

def cleanUp(vehicle):
    vehicle.clear()
    vehicle.close()



if __name__ == "__main__":
    while(True):
        #ARM rover 
        vehicle = rover.connect_to_rover()                      # connect Pi to Vale rover
        print(" Battery: %s" % vehicle.battery)
        rover.arm_rover(vehicle)                                # arm VALE motors

        # enter first speech to text phase
        speech.Begin_VALE()
        talking = speech.speech2text(speech.recog)
        speech.user_input(talking)
        bldngCode = speech.check_bldg(talking)

        #getting destination coordinates in long, lat
        if(bldngCode == 'ACAD'):
            destination = "-96.34073274639103, 30.61586894659058"
        elif(bldngCode == 'FERM'):
            destination = "-96.34204468234054, 30.617179856193943"
        elif(bldngCode == 'THOM'):
            destination = "-96.34152263572916, 30.617552472570498"
        elif(bldngCode == 'BLOC'):
            destination = "-96.34230349584688, 30.619087937692562"
        
        # enter routing phase
        currentPost = vehicle.location.global_relative_frame
        print("CurrentLocation = %s " % currentPost)
        plottedRoute = route.switchLatLong(route.parse_route(route.getRoute(destination)))

        for waypoint in plottedRoute:
            vehicle.simple_goto(waypoint)
        
        # enter second speech to text phase
