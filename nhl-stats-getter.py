import urllib2
import sys
import json
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

DEFAULT_URL = "http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2"
DEFAULT_FILE_NAME = "data.csv"
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

print "Parsing data on " + str(len(players_data)) + " players"
print "Loading out of " + DEFAULT_URL
print "Writing to " + DEFAULT_FILE_NAME
print "Pulling individual data from template: " + PLAYER_URL_PREFIX + "PLAYERID"

for category in CATEGORIES:
	output_file.write(category + ",")

output_file.write("\n")

for player in players_data:
	player_page = urllib2.urlopen(PLAYER_URL_PREFIX + str(player["playerId"])).read()
	miscellany = pull_miscellany(player_page)
	
	player["age"] = dob_to_age(miscellany["born"]).days/365.0
	player["shoots"] = miscellany["shoots"][0]
	player[""]
	
	for category in CATEGORIES:
		output_file.write(str(player[category])+",")

	output_file.write("\n")

print(bcolors.BOLD + bcolors.OKBLUE + "Done" + bcolors.ENDC)

def get_data():
	return players_data


