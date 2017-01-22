from influxdb import InfluxDBClient
import os
import re
import datetime
import calendar
from stravalib.client import Client

######### Variables ############

path_for_files = "./authfiles/"
influxhost = "localhost"
influxport = "8086"
influxuser = "root"
influxpassword = "root"
influxdbname = "strava"

strava = Client()
fluxdb = InfluxDBClient(influxhost, influxport, influxuser, influxpassword, influxdbname)


######### Functions ############


def initialise_db():
    print "...create database: ", influxdbname
    fluxdb.create_database(influxdbname)

    query = "select last(counter) from strava_activity"
    print "...queying last activity from DB" + influxdbname + " with query: '" + query + "'"

    result = list(fluxdb.query(query))
    print "...received result "

    db_results = []
    if result:
        for row in result[0]: counter = row.get("last")
        if counter == "None": counter = 0
        for row in result[0]: last_strava_activity = row.get("time")
        
        print "...last activity in DB " + influxdbname + " is: ", last_strava_activity

        db_results.append(counter)
        db_results.append(last_strava_activity)
    else:
        counter = 0
        last_strava_activity = "1970-01-01T00:00:01Z"

        print "...empty or no DB. getting all activities since 1970"
        
        db_results.append(counter)
        db_results.append(last_strava_activity)

    print "CCC", db_results
    return db_results



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




def convert_to_decimal_time(time):
    if len(time) == 3:
        time = "0" + time

    hour = int(time[:2])
    minute = float(time[-2:])
    minute = int((minute / 60) * 100)
    
    if minute < 10:
       minute = "0" + str(minute)

    return float(str(hour) + str(minute))
    



def convert_to_float(string):
    if not ('None' in string): 
        number = str(string)
        number = float(number)
        return number
    else: 
        return float(0)



def descriptive_bool(boolean):
    if boolean is True:
        return "yes"
    else:
        return "no"




def descriptive_bool_from_count(number):
    if number > 0:
        return "yes"
    else:
        return "no"




def descriptive_heartrate(max_heartrate):
    if (max_heartrate >= 175):
        return "High"
    elif (max_heartrate > 130) and (max_heartrate < 175):
        return "Average"
    elif (max_heartrate <= 129) and (max_heartrate < 50):
        return "Low"
    else:
        return "None"




def descriptive_temperature(avg_temp):
    if avg_temp == -999:
        return str("None")
    elif (avg_temp >= -100) and (avg_temp < 0):
        return str("Below zero")
    elif (avg_temp >= 0) and (avg_temp <= 10):
        return str("Cold")
    elif (avg_temp > 10) and (avg_temp <= 18):
        return str("Chilly")
    elif (avg_temp > 18) and (avg_temp <= 24):
        return str("Pleasant")
    elif (avg_temp > 24) and (avg_temp <= 30):
        return str("Warm")
    elif (avg_temp > 30) and (avg_temp < 999):
        return str("Hot")
    else:
        return str("None")
        



def descriptive_elapsed_time(time):
    if time < 3600:
        return str("Short")
    elif (time >= 3600) and (time < 18000):
        return str("Medium")
    else:
        return str("Long")




def descriptive_distance(distance):
    if distance < 10000:
        return str("Short")
    elif (distance >= 10000) and (distance < 50000):
        return str("Medium")
    elif (distance >= 50000) and (distance < 100000):
        return str("Long")
    else:
        return str("Gran Fondo")
 



def descriptive_start_time(start_time):
    if (start_time >= 500) and (start_time < 800):
       return str("Early morning")
    elif (start_time >= 800) and (start_time < 1100):
       return str("Morning")
    elif (start_time >= 1100) and (start_time < 1400):
       return str("Noon")
    elif (start_time >= 1400) and (start_time < 1800):
       return str("Afternoon")
    elif (start_time >= 1800) and (start_time < 2300):
       return str("Evening")
    elif (start_time >= 2300) and (start_time < 500):
       return str("Night")




def descriptive_workout_type(workout_type):
    if workout_type == "0":
        return str("Run: default")
    elif workout_type == "1":
        return str("Run: race")
    elif workout_type == "2":
        return str("Run: long run")
    elif workout_type == "3":
        return str("Run: workout")
    elif workout_type == "10":
        return str("Ride: default")
    elif workout_type == "11":
        return str("Ride: race")
    elif workout_type == "11":
        return str("Ride: workout")

 

def write_data_in_db(db_row):
    fluxdb.write_points(db_row)




def get_and_normalize_gravadata(counter, last_strava_activity):
    athlete = strava.get_athlete()
    athletename = athlete.lastname + " " + athlete.firstname

    activity_count = 0

    for activity in strava.get_activities(limit=5):
    #for activity in strava.get_activities(after=str(last_strava_activity)):
        counter += 1
        activity_count += 1
 
        distance = str(activity.distance)
        straight_length = convert_to_float(distance[:-2])
   
        average_speed = str(activity.average_speed)
        maximum_speed = str(activity.max_speed)
        average_watts = str(activity.average_watts)
   
        average_heartrate = str(activity.average_heartrate)
        maximum_heartrate = str(activity.max_heartrate)
        max_heartrate = maximum_heartrate
        if max_heartrate == "None":
            max_heartrate = int(-999)
    
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

        
        db_row = [{
            'measurement': 'strava_activity',
                'tags': {
                    'name': u'{0.name}'.format(activity),
                    'type': u'{0.type}'.format(activity),
                    #'location_city': u'{0.location_city}'.format(activity), #deprecated
                    #'location_country': u'{0.location_country}'.format(activity), #deprecated
                    'tracking_device_name': u'{0.device_name}'.format(activity),
                    'has_commute': descriptive_bool(activity.commute),
                    'was_on_trainer': descriptive_bool(activity.commute),
                    'is_flagged': descriptive_bool(activity.flagged),
                    'is_private': descriptive_bool(activity.private),
                    'has_comment': descriptive_bool_from_count(int(activity.comment_count)),
                    'was_with_other_athlete': descriptive_bool_from_count((int(activity.athlete_count) - 1)), 
                    'has_achievement': descriptive_bool_from_count(int(activity.achievement_count)),
                    'has_personal_records': descriptive_bool_from_count(int(activity.pr_count)),
                    'has_kudos': descriptive_bool_from_count(int(activity.kudos_count)),
                    'activity_id': u'{0.id}'.format(activity),
                    'year': activity.start_date.year,
                    'month': activity.start_date.month,
                    'weekday': calendar.day_name[activity.start_date.weekday()],
                    'time_of_day': descriptive_start_time(int(start_time)), 
                    'gear_name': gear_name,
                    'avg_temp': descriptive_temperature(avg_temp_desc),
                    'duration': descriptive_elapsed_time(int(elapsed_time)),
                    'straight_length': descriptive_distance(int(straight_length)),
                    'max_heartrate': descriptive_heartrate(max_heartrate),
                    'workout_type': descriptive_workout_type(str(activity.workout_type)),
                    'athlete': athletename,
                    'description': u'{0.description}'.format(activity)
                 },
                'time': u'{0.start_date}'.format(activity),
                'fields': {
                    'distance': straight_length,
                    'counter': int(counter),
                    'total_elevation_gain': convert_to_float(elevation[:-2]),
                    'average_speed': convert_to_float(average_speed[:-5]),
                    'average_heartrate': convert_to_float(average_heartrate),
                    'activity_time': u'{0.start_date}'.format(activity),
                    'start_time': convert_to_decimal_time(start_time),
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
        

        #print db_row
        print "...write activity id '" + u'{0.id}'.format(activity) + "' of user '" + athletename + "' to database:",influxdbname
        write_data_in_db(db_row)

    return int(activity_count)

######### Do stuff here ############

print "...initializing database"
gravadata_list = initialise_db()

print "...reading Strava API access token"
access_token = get_string_from_file('access_token')
strava.access_token = access_token

print "...retreiving data from strava API and normalize. looking for new activities since", gravadata_list[1]
entry_count = get_and_normalize_gravadata(gravadata_list[0], gravadata_list[1])

if entry_count == 0:
    print "...no new activities. finishing"    
else:
    print "...finished filling the database:", influxdbname    


