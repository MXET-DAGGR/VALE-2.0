from ublox_gps import UbloxGps
import serial
import spidev

# port= serial.Serial('/dev/serial0', baudrate=3400, timeout=1)
# gps=UbloxGps(port)
port=spidev.SpiDev()
gps=UbloxGps(port)


def run():
    try:
        print("Listening for UBX Messages. ")
        while True:
            try:
                gpsCords=gps.geo_coords()
                print(gpsCords.lat, gpsCords.lon, gpsCords.headMot)
            except(ValueError, IOError) as err:
                    print(err)
                    
    finally:
        port.close()
                
if __name__ == '__main__':
    run()