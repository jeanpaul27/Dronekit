#!/usr/bin/env python


from dronekit import connect, VehicleMode, LocationGlobalRelative
from geographiclib.geodesic import Geodesic

def calculate_waypoints(lat,lon,alt,box_size):
    """
    Function to create a box (size of box_size[m]) of waypoints around a selected location (lat,lon,alt)
    """
    waypoints = []
    for degree in range(0,360,45):
        waypoint = Geodesic.WGS84.Direct(lat,lon,degree,box_size)
        waypoints.append([waypoint['lat2'],waypoint['lon2'],alt])
    return waypoints

def get_distance_between_points(lat1,lon1,lat2,lon2):

 	"""
	Returns the distance in meters between two points (lat1,lon1) and (lat2,lon2)
 	"""
 	return Geodesic.WGS84.Inverse(lat1,lon1, lat2, lon2)['s12']


TARGET_ALTITUDE = 40
print('Conectandose al vehiculo')
vehicle = connect('127.0.0.1:14550',wait_ready = True)
print('Conectado. Chequeando si se puede armar')
while True:
    armable = vehicle.is_armable
    if armable: break
print('listo para armarse')
print('cambiando a modo guiado')
vehicle.mode = VehicleMode('GUIDED')
print('despegando')
vehicle.armed = True; vehicle.simple_takeoff(TARGET_ALTITUDE)
while True:
  if abs(TARGET_ALTITUDE - vehicle.location.global_relative_frame.alt) <= 1:
    print('Selected altitude was reached')
    break
  else:
    print('Current altitude: '+ str(vehicle.location.global_relative_frame.alt))

lat=2.148971
lon=-73.944397
alt=TARGET_ALTITUDE
box_size = 100
waypoints = calculate_waypoints(lat,lon,alt,box_size)

for wp in waypoints:
    location = LocationGlobalRelative(wp[0], wp[1], wp[2])
    vehicle.simple_goto(location)
    ## Wait till reaching the current waypoint
    while True:
        cP=vehicle.location.global_relative_frame.__dict__
        cla=cP['lat']
        clo=cP['lon']
        if get_distance_between_points(cla,clo,wp[0],wp[1]) < 1: break
vehicle.mode = VehicleMode("RTL")
