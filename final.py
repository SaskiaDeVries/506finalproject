import urllib
import requests
import json
import random
import unittest

# Used a Census Bureau file online to create a list of valid ZIP codes (i.e., recognized by Census API). Cached data provided.
try:
	#Open cached list of valid ZIP codes
	ziplist = open("validzipcodes.txt", 'r')
	zcta5_codes = json.loads(ziplist.read())
	ziplist.close()
except:
	# Open Census text file online and save it as a list of lines
	zcta5 = urllib.urlopen("http://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt")
	zcta5_lines = zcta5.readlines()
	zcta5.close()

	zcta5_codes = []
	# skip first line (variable names)
	for i in zcta5_lines[1:]:
		zipcode = i.split(",")
		# append the first item of each line (the ZIP code)
		zcta5_codes.append(zipcode[0])

	# save the list of valid ZIP codes as a text file
	zipcodes = open("validzipcodes.txt","w")
	zipcodes.write(json.dumps(zcta5_codes))
	zipcodes.close()

# defined a function to get a list of locations from the user 
def user_choice(lst):
	"""Function accepts a list of valid ZIP codes as input and prompts users to create a smaller list of ZIP codes"""
	# Ask users whether they want to enter ZIP codes or use a list of randomly selected ZIP codes
	prompt = raw_input("""In this program, you can compare populations across multiple ZIP codes.
		To enter your own ZIP codes of interest, enter 'own'. Otherwise enter 'random.' """)
	if prompt.lower() == 'own':
		locations = []
		# while loop used to allow users to select as many ZIP codes as they want.
		while True:
			user_zip = raw_input("""Please enter a valid ZIP code. Enter 'end' to stop adding ZIP codes. """)
			if user_zip.lower() == 'end':
				# break out of while loop when user enters 'end'
				break
			elif user_zip in lst:
				# append entered ZIP code if valid
				locations.append(user_zip)
			else:
				# print error message if text entered is not in the list of valid ZIP codes
				print "{} is not a valid ZIP code.".format(user_zip)
		return locations
	elif prompt.lower() == 'random':
		try:
			# if user enters something other than a number, the 'except' section assigns a value of 10
			zip_num = int(raw_input("How many ZIP codes do you want to compare? Limit is 50. "))
		except:
			print "Invalid input. 10 ZIP codes selected randomly."
			zip_num = 10
		locations = []
		if zip_num > 50 or zip_num < 1:
			print "Number out of range. 10 ZIP codes selected randomly."
			zip_num = 10
		for i in range(zip_num):
			# method randrange chooses an integer between 0 and the length of the list, and this is used as an index to select a ZIP code randomly.
			# The selected ZIP code is appended to the list of locations. This is repeated for the number of ZIP codes requested by the user.
			locations.append(lst[random.randrange(len(lst))])
		return locations
	else:
		# If users don't make a valid selection ('own' or 'random'), 10 ZIP codes are randomly selected.
		print "Invalid input. 10 ZIP codes selected randomly."
		locations = []
		for i in range(10):
			locations.append(lst[random.randrange(len(lst))])
		return locations

# API parameters for current weather by ZIP code using OpenWeatherMap API
# http://openweathermap.org/current

w_access_token = "0" # replace with OpenWeatherMap access token
w_baseurl = "http://api.openweathermap.org/data/2.5/weather"
w_url_params = {}
w_url_params["appid"] = w_access_token

# API parameters for Census ACS 5-Year Estimates using Census Bureau API
# http://www.census.gov/data/developers/data-sets/acs-5year.html
c_access_token = "0" # replace with Census access token
c_baseurl = "http://api.census.gov/data/2014/acs5"
c_url_params = {}
c_url_params["key"] = c_access_token
# variables requested are geography name, total population, and walked to work by race (white, black, AIAN, Asian, NHOPI, some other race, 2+ races)
c_url_params["get"] = "NAME,B01003_001E,B08105A_005E,B08105B_005E,B08105C_005E,B08105D_005E,B08105E_005E,B08105F_005E,B08105G_005E"

try:
	# open cached weather data
    w_f = open("weather_by_zip.txt", 'r')
    weather_list = json.loads(w_f.read())
    w_f.close()
    # open cached census data
    c_f = open("population_by_zip.txt", 'r')
    population_list = json.loads(c_f.read())
    c_f.close()
    
    # create a list of locations from the census data
    locations = []
    for i in population_list:
    	locations.append(i[1][-1])

    # Give users the option to get new data. (Ask after program checks if cached data possible. Without cached data, new data is only option.)
    override = raw_input("""Do you want to get new data? Enter 'yes' if so, otherwise enter any character: """)
    if override.lower() == 'yes':
    	raise # raises an exception to get new data through "except" code
except:
	# Prompt users for ZIP codes. Function returns a list of ZIP codes entered by user or chosen randomly.
	locations = user_choice(zcta5_codes)
	
	try:
		# Request weather data from the API and save in a list. API call made for each ZIP code returns a dictionary.
		weather_list = []
		for i in locations:
			w_url_params["zip"] = "{},us".format(i)
			r = requests.get(w_baseurl, params = w_url_params)
			zip_weather = json.loads(r.text)
			weather_list.append(zip_weather)
		# cache weather data
		w_f = open("weather_by_zip.txt",'w')
		w_f.write(json.dumps(weather_list))
		w_f.close()
	except:
		print "OpenWeatherMap API error. Check API key."
		exit()

	try:
		# Request census data from the API and save in a list. API call made for each ZIP code returns a list with two lists.
		population_list = []
		for i in locations:
			r = requests.get("http://api.census.gov/data/2014/acs5?get=NAME,B01003_001E,B08105A_005E,B08105B_005E,B08105C_005E,B08105D_005E,B08105E_005E,B08105F_005E,B08105G_005E&for=zip+code+tabulation+area:{}&key=2e225d1d74aabe94c2e39f2781606b904dbb6665".format(i))
			zip_pop = json.loads(r.text)
			population_list.append(zip_pop)
		# cache census data
		c_f = open("population_by_zip.txt",'w')
		c_f.write(json.dumps(population_list))
		c_f.close()
	except:
		print "Census API error. Check API key."
		exit()

# Add ZIP code to each weather dictionary (while used to call the API, it's not included in data from the API)
for i in range(len(locations)):
	addzip = locations[i]
	weather_list[i]["ZIPcode"] = addzip

class Weather():
	"""Object representing weather for a location defined by ZIP code"""
	def __init__(self, weather_dict={}):
		self.ZIPcode = weather_dict["ZIPcode"]
		self.name = weather_dict["name"] # location name
		self.sunset = weather_dict["sys"]["sunset"] # time of sunset (UTC)
		self.sunrise = weather_dict["sys"]["sunrise"] # time of sunrise (UTC)
		self.main = weather_dict["weather"][0]["main"] # one-word description of weather
		self.temp = weather_dict["main"]["temp"] # current temperature in Kelvin
		self.temp_min = weather_dict["main"]["temp_min"] # minimum current temperature in Kelvin (see README footnote)
		self.temp_max = weather_dict["main"]["temp_max"] # maximum current temperature in Kelvin (see README footnote)

	def temprange(self):
		# calculates the temperature range (returns degrees in Kelvin/Celcius)
		return self.temp_max - self.temp_min

	def temp_to_F(self, tempK):
		# converts Kelvin temperatures to Fahrenheit
		newtemp = tempK*(9.0/5) - 459.67
		return newtemp

	def temp_to_C(self, tempK):
		# converts Kelvin temperatures to Celcius
		newtemp = tempK - 273.15
		return newtemp

	def daylight(self):
		# calculates hours of daylight
		daylight = (self.sunset - self.sunrise)/3600.0
		return daylight

class Population():
	"""object representing population for a location"""
	def __init__(self, population_list=[]):
		self.ZIPcode = population_list[9]
		self.total = int(population_list[1]) # total population in ZIP code area
		self.white = int(population_list[2]) # walked to work, White
		self.black = int(population_list[3]) # walked to work, Black
		self.aian = int(population_list[4]) # walked to work, AIAN (American Indian and Alaska Native)
		self.asian = int(population_list[5]) # walked to work, Asian
		self.nhopi = int(population_list[6]) # walked to work, NHOPI (Native Hawaiian and Other Pacific Islanders)
		self.other = int(population_list[7]) # walked to work, other race
		self.twoplus = int(population_list[8]) # walked to work, 2 or more races

	def walked(self, population_list = []):
		# calculates population that walked to work by adding the number for each (mutually exclusive) race group
		walked = self.white+self.black+self.aian+self.asian+self.nhopi+self.other+self.twoplus
		return walked

	def percent_walked(self):
		# Some ZIP codes have population zero. The statement here avoids the error caused when program divides by zero
		if self.total == 0:
			return 0
		else:
			# calculates the percent of people who talk to work in a ZIP code
			walked = self.walked()
			total = self.total
			return 100*walked/float(total)

# For each ZIP code, creates an instance of the Weather class
weatherdata = [Weather(x) for x in weather_list]
# For each ZIP code, creates an instance of the Population class
popdata = [Population(x[1]) for x in population_list]

# Add data from instances of each class (Weather and Population) to a single dictionary called mashup
# Mashup is a dictionary where wach ZIP code is a key and the value is a dictionary of data for that ZIP code.
mashup = {}
for i in weatherdata:
	mashup[i.ZIPcode] = {}
	mashup[i.ZIPcode]["name"] = i.name
	mashup[i.ZIPcode]["daylight"] = i.daylight()
	mashup[i.ZIPcode]["weather_type"] = i.main
	mashup[i.ZIPcode]["temp_range_C"] = i.temprange()
	mashup[i.ZIPcode]["temp_min_C"] = i.temp_to_C(i.temp_min)
	mashup[i.ZIPcode]["temp_max_C"] = i.temp_to_C(i.temp_max)
	mashup[i.ZIPcode]["temp_range_F"] = i.temp_to_F(i.temp_max) - i.temp_to_F(i.temp_min)
	mashup[i.ZIPcode]["temp_min_F"] = i.temp_to_F(i.temp_min)
	mashup[i.ZIPcode]["temp_max_F"] = i.temp_to_F(i.temp_max)
for i in popdata:
	mashup[i.ZIPcode]["pop_total"] = i.total
	mashup[i.ZIPcode]["pop_walked"] = i.walked()
	mashup[i.ZIPcode]["percent_walked"] = i.percent_walked()

def walkers_by_weather_type(mashup):
	"""Function adds total number of walkers experiencing each type of weather, sorts weather type by the number of walkers, and then prints. Takes a dictionary as input."""
	# create an empty dictionary
	walk_by_weather = {}
	for zipcode in mashup:
		# add weather type to dictionary as a key and the number of people who walked as the value
		if mashup[zipcode]["weather_type"] not in walk_by_weather:
			# for each type of weather (key) the value is a dictionary with the population that walked to work and a list with the name of the location as keys
			walk_by_weather[mashup[zipcode]["weather_type"]] = {}
			walk_by_weather[mashup[zipcode]["weather_type"]]["pop_walked"] = mashup[zipcode]["pop_walked"]
			walk_by_weather[mashup[zipcode]["weather_type"]]["name"] = [mashup[zipcode]["name"]]
		else:
			# add to the population that walked to work experiencing each weather type
			walk_by_weather[mashup[zipcode]["weather_type"]]["pop_walked"] += mashup[zipcode]["pop_walked"]
			# add to the list of location names experiencing each weather type
			walk_by_weather[mashup[zipcode]["weather_type"]]["name"].append(mashup[zipcode]["name"])
	weather_type = walk_by_weather.keys()
	# sort list of weather types by the population that walked to work (highest to lowest)
	weather_sort = sorted(weather_type, key = lambda x: -walk_by_weather[x]["pop_walked"])
	for i in weather_sort:
		if i == "Clear":
			# "clear" is an adjective but the other weather words are nouns, so used a different sentence structure
			print "{} people walked to work experiencing {} weather in {}.".format(walk_by_weather[i]["pop_walked"],i.lower(),", ".join(walk_by_weather[i]["name"]))
		else:
			# print the number of people who (likely) walked to work in the weather type along with the list of the locations experiencing that weather
			print "{} people walked to work experiencing {} in {}.".format(walk_by_weather[i]["pop_walked"],i.lower(),", ".join(walk_by_weather[i]["name"]))

def location_by_percent_walked(mashup):
	"""Function sorts locations by percent walked and prints. Takes a dictionary as input"""
	# creates a list of tuples where each tuple has the place name, total population, and percent walking to work
	location_by_percent_walked = [(mashup[x]["name"], mashup[x]["pop_total"], round(mashup[x]["percent_walked"],1)) for x in mashup]
	# prints out the location names and percent who walked to work in each city, sorted by percent who walked to work (high to low) then alphabetical by place name for ties
	for i in sorted(location_by_percent_walked, key = lambda x: (-x[2], x[0])):
		print "In {} (population {}), {} percent of people walked to work.".format(*i)

def location_by_daylight_hours(mashup):
	"""Function sorts locations by hours of daylight and prints results. Takes a dictionary as input"""
	# creates a list of tuples where each tuple has the place name, total population, and the hours of daylight
	location_by_daylight = [(mashup[x]["name"], mashup[x]["pop_total"], round(mashup[x]["daylight"],1)) for x in mashup]
	# prints out the location names and hours of daylight, sorted by hours of daylight (high to low) then alphabetical by place name for ties
	for i in sorted(location_by_daylight, key = lambda x: (-x[2], x[0])):
		print "The time between sunrise and sunset in {} (population {}) is {} hours.".format(*i)

def location_by_temp_range(mashup):
	"""Function sorts locations by temperature range and prints results. Takes a dictionary as input asks users for degree units."""
	# creates a list of tuples where each tuple has the place name, total population, temperature range, min temp, and max temp (in celcius and fahrenheit).
	location_by_temprange = [(mashup[x]["name"], mashup[x]["pop_total"], mashup[x]["temp_range_C"], round(mashup[x]["temp_min_C"],1), round(mashup[x]["temp_max_C"],1), round(mashup[x]["temp_range_F"],1), round(mashup[x]["temp_min_F"],1), round(mashup[x]["temp_max_F"],1)) for x in mashup]
	degree = raw_input("Enter 'c' for Celcius or 'f' for Fahrenheit. ")
	while True:
		# checks whether users gave valid input. while-loop used to repeat question if users did not enter 'c' or 'f'
		if degree.lower() in ['c','f']:
			break
		if degree.lower() not in ['c','f']:
			degree = raw_input("Incorrect input. Enter 'c' for Celcius or 'f' for Fahrenheit. ")
	if degree.lower() == 'c':
		# sort by temperature range in celcius (large to small) and then alphabetical by place name for ties
		for i in sorted(location_by_temprange, key = lambda x: (-x[2], x[0])):
	 		print "The temperature range today in {} (population {}) is {} degrees: from {} to {} degrees Celcius.".format(*i[:5])
	elif degree.lower() == 'f':
		# sort by temperature range in fahrenheit (large to small) and then alphabetical by place name for ties
		for i in sorted(location_by_temprange, key = lambda x: (-x[5], x[0])):
	 		print "The temperature range in {} (population {}) is {} degrees: from {} to {} degrees Fahrenheit.".format(i[0], i[1], *i[5:])

# Ask users what type of data they want. Put in a while loop so people can make multiple requests. 
while True:
	user_request = raw_input("""\nWhat data do you want? Enter the number corresponding with the option you want, or 'end' to end the program.\n
		1. Number of people walking in each type of weather.\n
		2. Locations ranked by the percent of people walking to work.\n
		3. Locations ranked by the number of daylight hours. \n
		4. Locations ranked by the temperature range.\n
		Please enter your choice: """)
	# If no valid input, continue while loop to give user another chance.
	if user_request not in ['1','2','3','4','end']:
		print "\nInvalid input."
		continue
	elif user_request == '1':
		walkers_by_weather_type(mashup)
		print "\nYou can select again.\n"
	elif user_request == '2':
		location_by_percent_walked(mashup)
		print "\nYou can select again.\n"
	elif user_request == '3':
		location_by_daylight_hours(mashup)
		print "\nYou can select again.\n"
	elif user_request == '4':
		location_by_temp_range(mashup)
		print "\nYou can select again.\n"
	else:
		# Ends program if users enter 'end' (only way to reach this code)
		break

##### Code for running tests

class FinalProject(unittest.TestCase):
    def test_weatherdatatype(self):
        self.assertEqual(type(weather_list[0]), type({}), "Check the data from OpenWeatherMap is a dictionary for each ZIP code.")
    def test_popdatatype(self):
        self.assertEqual(type(population_list[0]), type([]), "Check the data from Census is a list for each ZIP code.")
    def test_weather_pop_length(self):
    	self.assertEqual(len(weatherdata),len(popdata), "Check the lists of Weather and Population instances are the same length.")
    def test_pop_total_type(self):
        self.assertEqual(type(popdata[0].total), type(1), "Check population totals are integers.")
    def test_dividebyzero(self):
    	self.assertEqual(popdata[0].percent_walked(), 0, "Check that percent_walked() does not try to divide by zero. Used ZIP code 63962 to test total population of zero.")
    def test_daylight_type(self):
        self.assertEqual(type(weatherdata[0].daylight()), type(1.0), "Check daylight function returns a float.")
    def test_convert_to_C(self):
    	self.assertEqual(weatherdata[0].temp_to_C(273.15), 0.0, "237.15 degrees Kelvin should convert to 0.0 degrees Celcius")
    def test_convert_to_F(self):
    	self.assertEqual(round(weatherdata[0].temp_to_F(273.15),1), 32.0, "237.15 degrees Kelvin should convert to 32.0 degrees Fahrenheit")

# runs unittests
unittest.main(verbosity=2)

