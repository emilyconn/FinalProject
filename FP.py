import requests, json, csv, plotly, sqlite3, secrets, unittest
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='emilyconn', api_key=secrets.plotlyapi)


conn = sqlite3.connect('FP.db')
cur = conn.cursor()

def set_up_db():

    cur.execute("""CREATE TABLE IF NOT EXISTS Yelp(Id integer primary key, Restaurant text, Rating real, Price text, Address text, type text, Phone text, City integer)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Cities(Id integer primary key, CityName text, State text, Lat text, Long text, Country text)""")
    conn.commit()


CACHE_FNAME = 'finalproj.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params, headers={}):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, headers=headers)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



def location_name(location, addToDB = False):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = make_request_using_cache(url, params={'address': location, 'key': secrets.googleapi})
    #print (response)
    cityname = response['results'][0]['address_components'][0]['long_name']
    state = response['results'][0]['address_components'][2]['long_name']
    lat = response['results'][0]['geometry']['location']['lat']
    lng = response['results'][0]['geometry']['location']['lng']
    try:
        country = response['results'][0]['address_components'][3]['short_name']
    except:
        country = None
    if addToDB:
        cur.execute('INSERT INTO Cities VALUES (?,?,?,?,?,?)', (None, cityname, state, lat, lng, country))
        conn.commit()
        #cur.execute('SELECT * FROM Cities WHERE ?1=CityName', (city,))
    return response['results'][0]['geometry']['location']

class YelpSearch():
    def __init__(self, city):
        self.CITY = city
        self.headers = {'Authorization': 'Bearer {}'.format(secrets.yelpapi)}
        self.coords = location_name(city)
        self.call_search = self.search()

    def search(self):
        url_params = {'longitude':self.coords['lng'],
                      "latitude":self.coords['lat'],
                      "limit":50,
                      "offset":50,
                      "radius":10000}

        response = make_request_using_cache('https://api.yelp.com/v3/businesses/search', headers = self.headers, params = url_params)
        self.YELP_RESPONSE = response
        #print (response)
        print ("Here is a list of 10 restaurant recommendations with their ratings:")
        for row in self.YELP_RESPONSE['businesses'][0:10]:
           print ("Suggestion: " + row['name'] + " (" + str(row['rating']) +")")
        #return self.YELP_RESPONSE

        for x in response['businesses']:
            restaurant = x['name']
            rating = x['rating']
            try:
                price = x['price']
            except:
                price = ''
            address = x['location']['address1']
            type = x['categories'][0]['alias']
            Phone = x['phone']
            cur.execute('SELECT * FROM Cities WHERE ?1=CityName', (self.CITY,))
            cityid = cur.fetchone()[0]
            cur.execute('INSERT INTO Yelp VALUES (?,?,?,?,?,?,?,?)', (None, restaurant, rating, price, address, type, Phone, cityid))
            conn.commit()

        url_params = {'longitude':self.coords['lng'],
                              "latitude":self.coords['lat'],
                              "limit":50,
                              "offset":50,
                              "radius":10000}

        response = make_request_using_cache('https://api.yelp.com/v3/businesses/search', headers = self.headers, params = url_params)
        self.YELP_RESPONSE = response

        for x in response['businesses']:
            restaurant = x['name']
            rating = x['rating']
            try:
                price = x['price']
            except:
                price = ''
            address = x['location']['address1']
            type = x['categories'][0]['alias']
            Phone = x['phone']
            cur.execute('SELECT * FROM Cities WHERE ?1=CityName', (self.CITY,))
            cityid = cur.fetchone()[0]
            cur.execute('INSERT INTO Yelp VALUES (?,?,?,?,?,?,?,?)', (None, restaurant, rating, price, address, type, Phone, cityid))
            conn.commit()

def visualA(city):

    #1
    type = cur.execute('SELECT type FROM Yelp JOIN Cities WHERE "{}" = CityName'.format(city))
    type_strings = [tup[0] for tup in cur.fetchall()]
    type_counts = {category : type_strings.count(category) for category in type_strings}
    data1 = [go.Bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values())

                )]
    layout1 = go.Layout(title = f'Number of Restaraunts in {city} by Type', xaxis=dict(title='Type of Restaurant'),
    yaxis=dict(title='Number of Restaurants'))
    fig = go.Figure(data=data1, layout=layout1)
    py.plot(fig, filename=f'Number of Restaraunts in {city} by Type')


def visualB(city):

    #2
    price = cur.execute('SELECT Price FROM Yelp JOIN Cities WHERE "{}" = CityName'.format(city))
    price_strings = [tup[0] for tup in cur.fetchall()]
    price_counts = {price : price_strings.count(price) for price in price_strings if price != ""}
    data2 = [go.Pie(
            labels=list(price_counts.keys()),
            values=list(price_counts.values())
    )]
    layout2 = go.Layout(title = f'Number of Restaraunts in {city} by Price Tier')
    fig = go.Figure(data=data2, layout=layout2)
    py.plot(fig, filename=f'Number of Restaraunts in {city} by Price Tier')


def visualC(city):

    ratings = cur.execute('SELECT Rating FROM Yelp JOIN Cities WHERE "{}"= CityName'.format(city))
    ratings_strings = [tup[0] for tup in cur.fetchall()]
    ratings_counts = {ratings : ratings_strings.count(ratings) for ratings in ratings_strings}

    data3 = [go.Bar(
            y=list(ratings_counts.keys()),
            x=list(ratings_counts.values()),
            orientation = "h"
    )]
    layout3 = go.Layout(title = f'Number of Restaraunts in {city} by Rating', xaxis=dict(title='Ratings Count'),
    yaxis=dict(title='Ratings'))
    fig = go.Figure(data=data3, layout=layout3)
    py.plot(fig, filename=f'Number of Restaraunts in {city} by Rating')



def visualD(city):

    ratings = cur.execute('SELECT Rating, Price FROM Yelp JOIN Cities WHERE "{}"= CityName'.format(city))
    results = cur.fetchall()
    price_list = [len(tup[1]) for tup in results]
    ratings_list = [tup[0] for tup in results]
    data4 = [go.Scatter(
            y=ratings_list,
            x=price_list,
            mode = 'markers'
    )]
    layout4 = go.Layout(title = f'Price v. Rating in {city}',
        xaxis=dict(title='Price List'),
        yaxis=dict(title='Ratings List'))
    fig = go.Figure(data=data4, layout=layout4)
    py.plot(fig, filename=f'Price v. Rating in {city}')



def main():
    while True:
        location = input("What is your location or 'exit' to quit: ").title()
        if location == 'exit'.title():
            break
        set_up_db()
        call_func = location_name(location, addToDB=True)
        call_func2 = YelpSearch(location)
        menu = input('If you would like to see grahs of the data, type "menu" for options or "exit" to quit: ')
        if menu == 'exit':
            break
        elif menu == 'menu':
            print ("""A: Bar Graph of the number of Restaraunts in the given location by Type
B: Pie chart of the Number of Restaraunts in the given location by Price Tier
C: Bar chart of Number of Restaraunts in the gievn location by Rating
D: Scatter plot of the Prive v. Rating in the given location
E: All of the graphs""")
            new_statement = input("Which graph would you like to see or 'exit' to quit: ").upper()
            if new_statement == 'A':
                visualA(location)
            elif new_statement == 'B':
                visualB(location)
            elif new_statement == 'C':
                visualC(location)
            elif new_statement == 'D':
                visualD(location)
            elif new_statement == 'E':
                visualA(location)
                visualB(location)
                visualC(location)
                visualD(location)
            elif new_statement == 'exit'.upper():
                break
            else:
                print ('Command not found')
                continue
        else:
            print ("Command not found.")
            continue


        conn.commit()



main()
