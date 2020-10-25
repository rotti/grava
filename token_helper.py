#!/usr/bin/env python3
import os
import requests
import urllib.request, urllib.error, urllib.parse
import json
import sys
import time
import webbrowser
from stravalib import Client
from stravalib.exc import AccessUnauthorized

# we need the files "client_id", "auth_code" and "client_secret" inside this path
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
        return None

def write_string_to_file(token_type, token_value):
    with open(path_for_files + token_type, "w") as token_file:
            token_file.write(token_value)
            print("...writing " + token_value + " to " + path_for_files + token_type)


def ensure_api_configured():
    print("Checking API configured")
    client_id = get_string_from_file('client_id')
    client_secret = get_string_from_file('client_secret')

    if not client_id or not client_secret:
        print("Not configured. Enter API details found at https://www.strava.com/settings/api")
        client_id = input("Client ID: ")
        client_secret = input("Client Secret: ")
        write_string_to_file("client_id", client_id)
        write_string_to_file("client_secret", client_secret)


def check_if_access_token_valid():
    print("Checking Access token valid")
    access_token = get_string_from_file('access_token')    
    strava = Client()
    try:
        strava.access_token = access_token
        strava.get_athlete()
    except AccessUnauthorized:
        print("Access Token not valid")
        return False
    print("Access Token valid. Exiting...")
    sys.exit(0)


def refresh_current_token():
    print("Refreshing current token")
    refresh_token = get_string_from_file('refresh_token')
    client_id = get_string_from_file('client_id')
    client_secret = get_string_from_file('client_secret')

    if not refresh_token:
        print("No refresh token present.")
        request_user_login()
    else:
        strava = Client()
        refresh_response = strava.refresh_access_token(client_id=client_id,
                                                       client_secret=client_secret,
                                                       refresh_token=refresh_token)

        write_string_to_file("access_token", refresh_response['access_token'])
        write_string_to_file("refresh_token", refresh_response['refresh_token'])
        
        check_if_access_token_valid()


def request_user_login():
    print("Requesting user login")

    client_id = get_string_from_file('client_id')
    client_secret = get_string_from_file('client_secret')

    client=Client()
    LOGIN_URL = client.authorization_url(client_id=client_id, redirect_uri='http://localhost')
    
    print(LOGIN_URL)
    webbrowser.open(LOGIN_URL)

    auth_code = input("Enter the auth_code from the redirected URL: ")
    write_string_to_file("auth_code", auth_code)

    token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=auth_code)

    write_string_to_file("access_token", token_response['access_token'])
    write_string_to_file("refresh_token", token_response['refresh_token'])
    
    check_if_access_token_valid()


def main():
    ensure_api_configured()
    check_if_access_token_valid()
    refresh_current_token()

    print("Something went wrong")
    sys.exit(1)

if __name__ == "__main__":
    main()
