#! /usr/bin/env python

import urllib2
import sys
import json
import time
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

GOAL_INFLATOR = 1
DEFAULT_URL = "http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20142015%20and%20gameTypeId=2"
DEFAULT_FILE_NAME = "data2014.csv"
PLAYER_URL_PREFIX = "http://www.nhl.com/ice/player.htm?id="

MISCELLANY_WANTED = ["Born", "Shoots"]
CATEGORIES = ["playerFirstName", "playerLastName", "playerId", "age", "seasonId", "shoots", "playerPositionCode", "playerTeamsPlayedFor", "gamesPlayed", "goals", "assists", "shots", "plusMinus", "penaltyMinutes", "timeOnIcePerGame", "shiftsPerGame"]

DOB_FORMAT = "%B %d, %Y"
NOW = datetime.today()

# HTML ELEMENT CONSTANTS
LI_END = "</li>"

def pull_miscellany(player_page):
	miscellany = {}
	for misc in MISCELLANY_WANTED:
		misc_key = misc+":</span> "
		value = player_page.find(misc_key)
		end_of_misc = player_page.find(LI_END, value)
		
		miscellany[misc.lower()] = player_page[value+len(misc_key):end_of_misc].strip()
	
	return miscellany

def dob_to_age(date_string):
	dob = datetime.strptime(date_string, DOB_FORMAT)
	return NOW - dob

response = urllib2.urlopen(DEFAULT_URL)
html_data = response.read()
players_data = json.loads(html_data)["data"]

output_file = open(DEFAULT_FILE_NAME, "w")

print bcolors.OKBLUE + "Parsing data on " + str(len(players_data)) + " players" + bcolors.ENDC
print bcolors.OKBLUE + "Loading out of " + DEFAULT_URL + bcolors.ENDC
print bcolors.OKBLUE + "Writing to " + DEFAULT_FILE_NAME + bcolors.ENDC
print bcolors.OKBLUE + "Pulling individual data from template: " + PLAYER_URL_PREFIX + "PLAYERID" + bcolors.ENDC
print bcolors.OKBLUE + "Using goal inflator: " + str(GOAL_INFLATOR) + bcolors.ENDC

for category in CATEGORIES:
	output_file.write(category.encode("utf-8") + ",")

output_file.write("\n")

for player in players_data:
	time.sleep(0.5) # So we don't kill the league's website

	player_page = urllib2.urlopen(PLAYER_URL_PREFIX + str(player["playerId"])).read()
	miscellany = pull_miscellany(player_page)
	
	player["age"] = dob_to_age(miscellany["born"]).days/365.0
	player["shoots"] = miscellany["shoots"][0]
	player["playerTeamsPlayedFor"] = player["playerTeamsPlayedFor"].replace(", ", "|")
	
	for category in CATEGORIES:
		if category in ("goals", "assists"):
			output_file.write(str(player[category] * GOAL_INFLATOR).encode("utf-8") + ",")
		elif type(player[category]) in (int, float):
			output_file.write(str(player[category]).encode("utf-8")+",")
		else:
			output_file.write(player[category].encode("utf-8")+",")

	output_file.write("\n")

print(bcolors.BOLD + bcolors.OKBLUE + "Done" + bcolors.ENDC)

def get_data():
	return players_data


