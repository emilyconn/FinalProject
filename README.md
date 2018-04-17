# FinalProject

Name: Emily Conn

Overview: This code uses Yelp API and the Google GeoCoding API to access the data necessary for the graphs and restaurant suggestions.
Both require an API key, so I have created a secrets.py file that has all of the API keys that I used in the project. 
My .gitignore hides secrets.py to keep my API keys hidden. The main class that helps to run my program is YelpSearch. 
YelpSearch takes in the Yelp API key and grants access to the information. It prints the suggestion list of restaurants and 
inserts the data in the database. The other main function is location_name. Location_name inserts the data from the Google Geocoding API 
which links the two tables, Cities and Yelp. 

Instructions:

1) Run FP.py on terminal
4) The code will now ask "What is your location or 'exit' to quit:" Type in your location. EX: Ann Arbor 
5) It will then print a list of 10 restaurants in the given location and will prompt you with another question. 
“If you would like to see graphs of the data, type "menu" for options or "exit" to quit:” Type in menu to see a list of options. 
6) After typing in menu, a list will pop up with different options for graphs. Pick your favorite option by typing the letter of the option.
2) Once all of the information is typed, the code will run plotly and the graphs will print. 

Here are a few examples of interactions with the code:

Emilys-MBP-2:FinalProj andrewconn$ python3 FP.py 
What is your location or 'exit' to quit: Ann Arbor
Here is a list of 10 restaurant recommendations with their ratings:
Suggestion: Belly Deli (4.0)
Suggestion: Broadway Cafe & Hoagie (4.5)
Suggestion: Grange Kitchen & Bar (3.5)
Suggestion: Avalon Cafe and Kitchen (4.0)
Suggestion: Pilar's Tamales (4.5)
Suggestion: The Earle Restaurant (3.5)
Suggestion: Gratzi (3.5)
Suggestion: Wolverine State Brewing Co (4.5)
Suggestion: Jerusalem Garden (4.0)
Suggestion: The Ravens Club (3.5)
If you would like to see graphs of the data, type "menu" for options or "exit" to quit: menu
A: Bar Graph of the number of Restaraunts in the given location by Type
B: Pie chart of the Number of Restaraunts in the given location by Price Tier
C: Bar chart of Number of Restaraunts in the gievn location by Rating
D: Scatter plot of the Prive v. Rating in the given location
E: All of the graphs
Which graph would you like to see or 'exit' to quit: E 


Emilys-MBP-2:FinalProj andrewconn$ python3 FP.py 
What is your location or 'exit' to quit: maple glen
Here is a list of 10 restaurant recommendations with their ratings:
Suggestion: The Metropolitan (4.0)
Suggestion: Alice Bakery & Confectionary (4.0)
Suggestion: Pumpernick's Deli (4.0)
Suggestion: Wissahickon Valley Trail (4.5)
Suggestion: Bonefish Grill (3.5)
Suggestion: Anne's Kitchen Table (4.5)
Suggestion: R&R Caribbean Cuisine (4.5)
Suggestion: Lancers Diner (3.5)
Suggestion: Pho Viet Hoa (4.0)
Suggestion: Tonelli's Pizza Pub (3.5)
If you would like to see graphs of the data, type "menu" for options or "exit" to quit: menu
A: Bar Graph of the number of Restaraunts in the given location by Type
B: Pie chart of the Number of Restaraunts in the given location by Price Tier
C: Bar chart of Number of Restaraunts in the gievn location by Rating
D: Scatter plot of the Prive v. Rating in the given location
E: All of the graphs
Which graph would you like to see or 'exit' to quit: a


Emilys-MBP-2:FinalProj andrewconn$ python3 FP.py 
What is your location or 'exit' to quit: Detroit
Here is a list of 10 restaurant recommendations with their ratings:
Suggestion: Avalon International Breads (4.5)
Suggestion: Wala (4.5)
Suggestion: ASHE Supply Co (4.5)
Suggestion: Honey Bee La Colmena (4.5)
Suggestion: Downtown Louie's (4.0)
Suggestion: Red Smoke Barbecue (3.5)
Suggestion: Firebird Tavern (4.0)
Suggestion: Takoi (4.5)
Suggestion: Shake Shack (3.5)
Suggestion: Bobcat Bonnie's (4.0)
If you would like to see graphs of the data, type "menu" for options or "exit" to quit: menu
A: Bar Graph of the number of Restaraunts in the given location by Type
B: Pie chart of the Number of Restaraunts in the given location by Price Tier
C: Bar chart of Number of Restaraunts in the gievn location by Rating
D: Scatter plot of the Prive v. Rating in the given location
E: All of the graphs
Which graph would you like to see or 'exit' to quit: b
