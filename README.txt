506 Final Project

1. Describe your project in 1-4 sentences. Include the basic summary of what it does, and the output that it should generate/how one can use the output and/or what question the output answers. 

The project mashes up weather data and population data to see how many people experienced each type of weather on their walk to work today, and explores other conditions related to commute conditions (percent of people walking to work, daylight hours, and temperature range). If users do not choose cached data, they are promted to enter ZIP codes of interest or allow the program to randomly select a number of ZIP codes of their choice to compare. The program then asks users to choose among four report options where sentences are constructed (and sorted) based on the data: (1) Number of people walking in each type of weather, (2) Locations ranked by the percent of people walking to work, (3) Locations ranked by the number of daylight hours, and (4) Locations ranked by the temperature range. This output answers the questions of how many people are experiencing a type of weather while walking (1), how common it it to walk to work (2), and the general commute conditions for all people in a location (3) & (4).

2. Explain exactly what needs to be done to run your program (what file to run, anything the user needs to input, anything else) and what we should see once it is done running (should it have created a new text file or CSV? What should it basically look like?). (Your program running should depend on cached data, but OK to write a program that would make more sense to run on live data and tell us to e.g. use a sample value in order to run it on cached data.)

Files you need in the same folder:
 - final.py
 - weather_by_zip.txt
 - population_by_zip.txt
 - validzipcodes.txt

How to run the program:
 1. Run python final.py
 2. When asked whether to get new data, press any key and hit enter (do NOT enter 'yes')
 3. When asked for data to view, press '1' and hit enter (then repeat three more times, entering 2, 3, and 4)
 4. Output will be printed in the terminal window
 5. Type 'end' and press enter to end the program

3. List all the files you are turning in, with a brief description of each one. (At minimum, there should be 1 Python file, 1 file containing cached data, and the README file, but if your project requires others, that is fine as well! Just make sure you have submitted them all.)

 - final.py 					--> This file contains all of the code for the project.
 - weather_by_zip.txt 			--> This file is a list of dictionaries with cached weather data.
 - population_by_zip.txt 		--> This file is a list of lists with cached census ACS data.
 - validzipcodes.txt			--> This file is a list of all ZIP codes recognized by the Census API
 - README.txt 					--> Current file with overview of program and instructions for running it
 - 506 Final Project Screen *.png --> Five screen shots of the program running

4. Any Python packages/modules that must be installed in order to run your project (e.g. requests, or requests_oauthlib, or...):

 - urllib
 - requests
 - json
 - random
 - unittest

5. What API sources did you use? Provide links here and any other description necessary.

 - OpenWeatherMaps current weather API which allows calls by ZIP code: http://openweathermap.org/current
 - Census Bureau's American Community Survey 5-year estimates API (for 2009-2014 data): http://www.census.gov/data/developers/data-sets/acs-5year.html

6. Approximate line numbers in Python file to find the following mechanics requirements (this is so we can grade your code!):
- Sorting with a key function:
	252, 266, 274, 290, 294
- Use of list comprehension OR map OR filter:
	211, 213, 264, 272, 280
- Class definition beginning 1:
	151
- Class definition beginning 2:
	182
- Creating instance of one class:
	211
- Creating instance of a second class:
	213
- Calling any method on any class instance (list all approx line numbers where this happens, or line numbers where there is a chunk of code in which a bunch of methods are invoked):
	221 - 232
- (If applicable) Beginnings of function definitions outside classes:
	32, 234, 261, 269, 277
- Beginning of code that handles data caching/using cached data:
	8-29 (zipcodes), 92-144 (weather & population data)
- Test cases: 
	327 - 345

8. Rationale for project: why did you do this project? Why did you find it interesting? Did it work out the way you expected?

I chose this project because I wanted to use population data, and I thought pairing weather with the (expected) number of people walking to work would be interesting. (It was inspired by the challenge of walking/biking around Ann Arbor in December weather. I wanted to know how many other people could commiserate). The project generally worked out the way I expected, although I ended up defining more functions outside of the classes than expected. I wanted the user to have several opportunities to interact with the data, and it seemed easier to write the functions for each of those interactions separately. It seems much cleaner to call a function after raw_input instead of another 10 lines of code. It was fun to think through all of the ways users might ignore instructions, and then plan overrides.

* Note on data: The weather min and max (and thus calculated range) are the *current* min and max. There is a range for large cities and geographically expanded areas where one location name may cover multiple ZIP codes (e.g., San Francisco County). Additionally, population data is specific to the ZIP code, not the entire location covered by a name. For example, the cached data shows Oklahoma City with a population of 4,328, but this is the population in a ZIP code randomly selected which falls within Oklahoma City. The city itself contains several ZIP codes, so reporting the total population of the city would require knowing all of those ZIP codes (beyond the scope of this project). Finally, the data on walked to work is based on people's usual commuting habits, but it's reasonable to expect seasonal variation. The true number of people walking to work in extreme weather is likely lower than the reported number.

