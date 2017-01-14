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
influxdbname = "strava"

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



access_token = get_string_from_file('access_token')
strava.access_token = access_token


athlete = strava.get_athlete()
athletename = athlete.lastname + " " + athlete.firstname

counter = 0

print "...retreiving data from strava"
#for activity in strava.get_activities(limit=2):
for activity in strava.get_activities():
    counter += 1
 
    distance = str(activity.distance)
    elevation = str(activity.total_elevation_gain)
    average_speed = str(activity.average_speed)
    maximum_speed = str(activity.max_speed)
    average_heartrate = str(activity.average_heartrate)
    maximum_heartrate = str(activity.max_heartrate)

    gear_name = str(activity.gear_id)
    if not gear_name == "None":
        gear_name = strava.get_gear(gear_name).name

    elev_high = str(activity.elev_high)    
    elev_low = str(activity.elev_low)    

    calories = str(activity.calories)
    kilojoules = str(activity.kilojoules)
    start_time = str(activity.start_date)[11:16].replace(':', '')
    kudos_count = str(activity.kudos_count)
    achievement_count = str(activity.achievement_count)
    comment_count= str(activity.comment_count)
    athlete_count = str(activity.athlete_count)
    pr_count = str(activity.pr_count)
    average_temp = str(activity.average_temp)
    average_watts = str(activity.average_watts)

    workout_type = str(activity.workout_type)
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

         
    d = [{
        'measurement': 'strava_activity',
            'tags': {
                'name': u'{0.name}'.format(activity),
                'type': u'{0.type}'.format(activity),
                #'location_city': u'{0.location_city}'.format(activity), #deprecated
                #'location_country': u'{0.location_country}'.format(activity), #deprecated
                'device_name': u'{0.device_name}'.format(activity),
                'commute': u'{0.commute}'.format(activity),
                'trainer': u'{0.trainer}'.format(activity),
                'flagged': u'{0.flagged}'.format(activity),
                'activity_id': u'{0.id}'.format(activity),
                'gear_name:': gear_name,
                'activity_counter:': counter,
                'tag_average_temp': convert_to_float(average_temp),
                'tag_start_time': convert_to_float(start_time),
                'tag_elev_high': convert_to_float(elev_high),
                'tag_elev_low': convert_to_float(elev_low),
                'tag_distance': convert_to_float(distance[:-2]),
                'tag_total_elevation_gain': convert_to_float(elevation[:-2]),
                'tag_average_speed': convert_to_float(average_speed[:-5]),
                'tag_average_heartrate': convert_to_float(average_heartrate),
                'tag_activity_time': u'{0.start_date}'.format(activity),
                'tag_calories': convert_to_float(calories),
                'tag_kilojoules': convert_to_float(kilojoules),
                'tag_max_speed': convert_to_float(maximum_speed[:-6]),
                'tag_max_heartrate': convert_to_float(maximum_heartrate),
                'tag_average_watts': convert_to_float(average_watts),
                'tag_elapsed_time': convert_to_seconds(u'{0.elapsed_time}'.format(activity)),
                'tag_moving_time': convert_to_seconds(u'{0.moving_time}'.format(activity)),
                'tag_comment_count': convert_to_float(comment_count), 
                'tag_athlete_count': convert_to_float(athlete_count),
                'tag_achievement_count': convert_to_float(achievement_count), 
                'tag_pr_count': convert_to_float(pr_count),
                'tag_kudos_count': convert_to_float(kudos_count),
                'workout_type': workout_type,
                'athlete:': athletename,
                'description': u'{0.description}'.format(activity)
             },
            'time': u'{0.start_date}'.format(activity),
            'fields': {
                'distance': convert_to_float(distance[:-2]),
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
                'elapsed_time': convert_to_seconds(u'{0.elapsed_time}'.format(activity)),
                'moving_time': convert_to_seconds(u'{0.moving_time}'.format(activity))
             }
      }]
        

    #print d
    print "...write activity id '" + u'{0.id}'.format(activity) + "' of user '" + athletename + "' as entry '" + str(counter) + "' to database:",influxdbname 
    fluxdb.write_points(d)

print "...finished filling the database:", influxdbname    


