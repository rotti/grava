from influxdb import InfluxDBClient
import os
import json
import simplejson
import re
import datetime
from stravalib.client import Client
#XXX json still necessary


path_for_files = "./authfiles/"
influxhost = "localhost"
influxport = "8086"
influxuser = "root"
influxpassword = "root"
influxdbname = "test"

strava = Client()
fluxdb = InfluxDBClient(influxhost, influxport, influxuser, influxpassword, influxdbname)


print "...create database: ", influxdbname
fluxdb.create_database(influxdbname)



def get_string_from_file(file):
    if os.path.exists(path_for_files + file):
        with open(path_for_files + file, 'r') as string_from_file:
            global string
            string = string_from_file.read().replace('\n', '')
            print "...reading " + path_for_files + file 
            print "...reading ", file 
            print "...getting ", string 
            return string
    else:
        sys.exit("...exiting. cannot find " + path_for_files + file)




def convert_to_seconds(time):
    if not (' ' in time):
        h,m,s = re.split(':', time)
        return float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
    else: 
        return float(0)




def convert_to_float(string):
    if not ('None' in string): 
        number = str(string)
        number = float(number)
        return number
    else: 
        return float(0)



def boolean_to_string(boolean, string):
    if boolean is True:
        return string + ": yes"
    else:
        return string + ": no"




def create_boolean_string_from_number(number, string):
    if number > 0:
        return string + ": yes"
    else:
        return string + ": no"




def descriptive_heartrate(max_heartrate):
    if (max_heartrate >= 175):
        return "High"
    elif (max_heartrate > 130) and (max_heartrate < 175):
        return "Average"
    else:
        return "Low"




def descriptive_temperature(avg_temp):
    if avg_temp == -999:
        return "None"
    elif (avg_temp >= -100) and (avg_temp < 0):
        return "Below zero"
    elif (avg_temp >= 0) and (avg_temp <= 10):
        return "Cold"
    elif (avg_temp > 10) and (avg_temp <= 18):
        return "Chilly"
    elif (avg_temp > 18) and (avg_temp <= 24):
        return "Pleasant"
    elif (avg_temp > 24) and (avg_temp <= 30):
        return "Warm"
    elif (avg_temp > 30) and (avg_temp < 999):
        return "Hot"
    else:
        return "None"
        



def descriptive_elapsed_time(time):
    if time < 3600:
        return "Short"
    elif (time >= 3600) and (time < 18000):
        return "Medium"
    else:
        return "Long"




def descriptive_distance(distance):
    if distance < 10000:
        return "Short"
    elif (distance >= 10000) and (distance < 50000):
        return "Medium"
    elif (distance >= 50000) and (distance < 100000):
        return "Long"
    else:
        return "Gran Fondo"
 



def descriptive_start_time(start_time):
    if (start_time >= 500) and (start_time < 800):
       return "Early morning"
    elif (start_time >= 800) and (start_time < 1100):
       return "Morning"
    elif (start_time >= 1100) and (start_time < 1400):
       return "Noon"
    elif (start_time >= 1400) and (start_time < 1800):
       return "Afternoon"
    elif (start_time >= 1800) and (start_time < 2300):
       return "Evening"
    elif (start_time >= 2300) and (start_time < 500):
       return "Night"




def descriptive_workout_type(workout_type):
    if workout_type == "0":
        workout_type = str("Run: default")
    elif workout_type == "1":
        workout_type = str("Run: race")
    elif workout_type == "2":
        workout_type = str("Run: long run")
    elif workout_type == "3":
        workout_type = str("Run: workout")
    elif workout_type == "10":
        workout_type = str("Ride: default")
    elif workout_type == "11":
        workout_type = str("Ride: race")
    elif workout_type == "11":
        workout_type = str("Ride: workout")

    return workout_type
 



access_token = get_string_from_file('access_token')
strava.access_token = access_token

athlete = strava.get_athlete()
athletename = athlete.lastname + " " + athlete.firstname

counter = 0

print "...retreiving data from strava"
for activity in strava.get_activities(limit=3):
#for activity in strava.get_activities():
    counter += 1
 
    distance = str(activity.distance)
    straight_length = convert_to_float(distance[:-2])
   
    average_speed = str(activity.average_speed)
    maximum_speed = str(activity.max_speed)
    average_watts = str(activity.average_watts)
   
    average_heartrate = str(activity.average_heartrate)
    maximum_heartrate = str(activity.max_heartrate)
    
    elapsed_time = convert_to_seconds(str(activity.elapsed_time))
    start_time = str(activity.start_date)[11:16].replace(':', '')

    gear_name = str(activity.gear_id)
    if not gear_name == "None":
        gear_name = strava.get_gear(gear_name).name

    elevation = str(activity.total_elevation_gain)
    elev_high = str(activity.elev_high)    
    elev_low = str(activity.elev_low)    

    calories = str(activity.calories)
    kilojoules = str(activity.kilojoules)
    
    kudos_count = str(activity.kudos_count)
    achievement_count = str(activity.achievement_count)
    comment_count= str(activity.comment_count)
    athlete_count = str(activity.athlete_count)
    pr_count = str(activity.pr_count)
   
    average_temp = str(activity.average_temp)
    avg_temp_desc = average_temp
    if avg_temp_desc == "None":
        avg_temp = int(-999)

        
    d = [{
        'measurement': 'strava_activity',
            'tags': {
                'name': u'{0.name}'.format(activity),
                'type': u'{0.type}'.format(activity),
                #'location_city': u'{0.location_city}'.format(activity), #deprecated
                #'location_country': u'{0.location_country}'.format(activity), #deprecated
                'device_name': u'{0.device_name}'.format(activity),
                'commute': boolean_to_string(activity.commute, "Commute"),
                'trainer': boolean_to_string(activity.commute, "Trainer"),
                'flagged': boolean_to_string(activity.flagged, "Flagged"),
                'private': boolean_to_string(activity.private, "Private"),
                'comment': create_boolean_string_from_number(int(activity.comment_count), "Was commented"),
                'athlete': create_boolean_string_from_number((int(activity.athlete_count) - 1), "Was joint"), 
                'achievement': create_boolean_string_from_number(int(activity.achievement_count), "Has achievements"),
                'personal_records': create_boolean_string_from_number(int(activity.pr_count), "Has personal records"),
                'kudos': create_boolean_string_from_number(int(activity.kudos_count), "Has Kudos"),
                'activity_id': u'{0.id}'.format(activity),
                'gear_name:': gear_name,
                'activity_counter:': counter,
                'avg_temp': descriptive_temperature(avg_temp_desc),
                'duration': descriptive_elapsed_time(int(elapsed_time)),
                'time_of_day': descriptive_start_time(int(start_time)), 
                'straight_length': descriptive_distance(int(straight_length)),
                'max_heartrate': descriptive_heartrate(int(activity.max_heartrate)),
                'workout_type': descriptive_workout_type(str(activity.workout_type)),
                'athlete:': athletename,
                'description': u'{0.description}'.format(activity)
             },
            'time': u'{0.start_date}'.format(activity),
            'fields': {
                'distance': straight_length,
                'total_elevation_gain': convert_to_float(elevation[:-2]),
                'average_speed': convert_to_float(average_speed[:-5]),
                'average_heartrate': convert_to_float(average_heartrate),
                'activity_time': u'{0.start_date}'.format(activity),
                'start_time': convert_to_float(start_time),
                'elev_high': convert_to_float(elev_high),
                'elev_low': convert_to_float(elev_low),
                'calories': convert_to_float(calories),
                'kilojoules': convert_to_float(kilojoules),
                'max_speed': convert_to_float(maximum_speed[:-6]),
                'max_heartrate': convert_to_float(maximum_heartrate),
                'comment_count': convert_to_float(comment_count), 
                'athlete_count': convert_to_float(athlete_count),
                'achievement_count': convert_to_float(achievement_count), 
                'kudos_count': convert_to_float(kudos_count),
                'pr_count': convert_to_float(pr_count),
                'average_temp': convert_to_float(average_temp),
                'average_watts': convert_to_float(average_watts),
                'elapsed_time': elapsed_time,
                'moving_time': convert_to_seconds(u'{0.moving_time}'.format(activity))
             }
      }]
        

    print d
    print "...write activity id '" + u'{0.id}'.format(activity) + "' of user '" + athletename + "' as entry '" + str(counter) + "' to database:",influxdbname 
    fluxdb.write_points(d)

print "...finished filling the database:", influxdbname    


