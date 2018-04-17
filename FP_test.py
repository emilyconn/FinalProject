import unittest, FP, sqlite3

conn = sqlite3.connect('FP.db')
cur = conn.cursor()

class TestDataAccess(unittest.TestCase):


    def test_data_access(self):
        x = FP.location_name('Ann Arbor')
        self.assertTrue(type(x) == dict)
        self.assertTrue(x.keys(), ['lat', 'lng'])
        self.assertTrue(x.values(), [42.2808256, -83.7430378])
        self.assertTrue(type(x.keys()), list)
        self.assertTrue(type(x.values()), list)

class TestStorage(unittest.TestCase):

    def test_data_storage(self):
        cur.execute('SELECT * FROM Cities')
        results= cur.fetchall()
        self.assertTrue(len(results) > 0)
        self.assertTrue(type(results) == list)
        self.assertTrue(type(results[0]) == tuple)
        self.assertTrue(len(results[0]) == 6)

class TestProcessingComponents(unittest.TestCase):


    def test_processing_data_visualA(self):

        type = cur.execute('SELECT type FROM Yelp JOIN Cities WHERE "{}" = CityName'.format('Ann Arbor'))
        type_strings = [tup[0] for tup in cur.fetchall()]
        type_counts = {category : type_strings.count(category) for category in type_strings}
        self.assertTrue(type_counts.keys(), ['korean', 'newamerican', 'cafes', 'latin', 'wine_bars', 'italian', 'pubs', 'desserts',
        'tradamerican', 'bbq', 'seafood', 'pizza', 'breakfast_brunch', 'irish', 'delis', 'sushi', 'ethiopian', 'gaybars', 'japanese',
        'mexican', 'sandwiches', 'diners', 'steak', 'mideastern', 'divebars', 'lounges', 'localflavor',
        'coffee', 'food_court', 'tex-mex', 'indpak','chinese', 'polish', 'bars'])
        self.assertTrue(type_counts.values(), [ 8, 6, 4, 2, 2, 4, 4, 2, 4, 2, 2, 6, 2, 2, 4, 2, 2, 2, 4, 4, 2, 4, 2, 4, 2, 2, 2, 2,
        2, 2, 2,2, 2,2])

    def test_processing_data_visualB(self):
        price = cur.execute('SELECT Price FROM Yelp JOIN Cities WHERE "{}" = CityName'.format('Ann Arbor'))
        price_strings = [tup[0] for tup in cur.fetchall()]
        price_counts = {price : price_strings.count(price) for price in price_strings if price != ""}
        self.assertTrue(price_counts.keys(), ['$', '$$$', '$$'])
        self.assertTrue(price_counts.values(), [30, 10, 58])

    def test_processing_data_visualC(self):

        ratings = cur.execute('SELECT Rating FROM Yelp JOIN Cities WHERE "{}"= CityName'.format('Ann Arbor'))
        ratings_strings = [tup[0] for tup in cur.fetchall()]
        ratings_counts = {ratings : ratings_strings.count(ratings) for ratings in ratings_strings}
        self.assertTrue(ratings_counts.keys(), [4.0, 4.5, 3.5, 5.0])
        self.assertTrue(ratings_counts.values(), [36, 20, 42, 2])

    def test_processing_data_visualD(self):
        ratings = cur.execute('SELECT Rating, Price FROM Yelp JOIN Cities WHERE "{}"= CityName'.format('Ann Arbor'))
        results = cur.fetchall()
        price_list = [len(tup[1]) for tup in results]
        ratings_list = [tup[0] for tup in results]
        self.assertTrue(len(price_list), 100)
        self.assertTrue(type(ratings_list), list)

unittest.main()
