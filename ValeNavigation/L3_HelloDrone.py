print("Hello drone")
from dronekit import connect, VehicleMode

#UDP endpoint on the RPi
connection_string = "/dev/ttyAMA0"

#creating a vehicle endpoint
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready = True, baud= 921600)
vehicle.wait_ready(True, raise_exception=False)


# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable

vehicle._wp_uploaded


# Close vehicle object before exiting script
vehicle.close()
print("end of HelloDrone")
