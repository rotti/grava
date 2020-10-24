#!/usr/bin/env python3
import os
import requests
import urllib.request, urllib.error, urllib.parse
import json
import sys
import time
import webbrowser

# we need the files "client_id", "auth_code" and "strava_secret" inside this path
# if you change the path, dont forget to .gitignore it
path_for_files = "./authfiles/"


def internet_on():
    try:
        response=urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib.error.URLError as err: pass
    return False

if not internet_on():
    sys.exit("...exiting. no internet connection")


def get_string_from_file(file):
    if os.path.exists(path_for_files + file):
        with open(path_for_files + file, 'r') as string_from_file:
            global string
            string = string_from_file.read().replace('\n', '')
            print("...reading " + path_for_files + file)
            if not string:
                sys.exit("...exiting." + path_for_files + file + "is empty")
            else:
                print("...getting ", string + "\n")
            return string
    else:
        sys.exit("...exiting. cannot find " + path_for_files + file)



# uncomment the following section for getting your "code". (afterwards put the comments in again)
# this will open a webbrowser. you have to login to Strava and allow Korekuta to connect to Strava
# afterwards you will get an "Unable to connect" failure. But you will receive your tempory code
# it will look something like "http://localhost/token_exchange?state=mystate&code=1d1de858d2005b56e02d16d657cfad8bbc769a6f"
# copy the "code" as a string in the file "auth_code" in your authfiles directory

# start uncommenting beneath here. put comments in aferwards an run token_helper again

#client_id = get_string_from_file('client_id')
#LOGIN_URL = 'https://www.strava.com/oauth/authorize?client_id='+ client_id + '&response_type=code&redirect_uri=http://localhost/exchange_token&scope=read&state=mystate&approval_prompt=force'
#webbrowser.open(LOGIN_URL)
#time.sleep(1500)

# stop uncommenting here ;)


# get the secret token and write it to a file 
auth_code = get_string_from_file('auth_code')
strava_secret = get_string_from_file('strava_secret')
client_id = get_string_from_file('client_id')
AUTH_URL = "https://www.strava.com/oauth/token"
strava_forms = {
    'client_id': client_id,
    'client_secret': strava_secret,
    'code': auth_code  
}

session = requests.session()
request = requests.post(AUTH_URL, data=strava_forms)
print("...reading access token from " + AUTH_URL)

response = request.json()
token = response['access_token']
print("...getting access token ",token)

with open(path_for_files + "access_token", "w") as access_token:
        access_token.write(token)
        print("...writing access token to " + path_for_files + "access_token")
