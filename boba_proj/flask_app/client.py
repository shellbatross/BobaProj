import requests

"""
Doing API calls here to check the Ninja Calorie API
"""
#Might change later to have the caloric info
class Boba:
    def __init__(self, price, name):
        self.name = name
        self.price = price

    def __repr__(self):
        return self.name


#Gonna change this to make links instead to get the calorie information 
class MovieClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&r=json&type=movie&"

    def search(self, search_string):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        search_string = "+".join(search_string.split())
        page = 1

        search_url = f"s={search_string}&page={page}"

        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        search_results_json = data["Search"]
        remaining_results = int(data["totalResults"])

        result = []

        ## We may have more results than are first displayed
        while remaining_results != 0:
            for item_json in search_results_json:
                result.append(Movie(item_json))
                remaining_results -= len(search_results_json)
            page += 1
            search_url = f"s={search_string}&page={page}"
            resp = self.sess.get(self.base_url + search_url)
            if resp.status_code != 200 or resp.json()["Response"] == "False":
                break
            search_results_json = resp.json()["Search"]

        return result

    def retrieve_movie_by_id(self, imdb_id):
        """
        Use to obtain a Movie object representing the movie identified by
        the supplied imdb_id
        """
        movie_url = self.base_url + f"i={imdb_id}&plot=full"

        resp = self.sess.get(movie_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'Error retrieving results: \'{data["Error"]}\' ')

        movie = Movie(data, detailed=True)

        return movie
    #IDKNO WHAT X IS, IT SAID I WAS SENDING TWO THINGS HERE LMAO BUT IT WORKS BRO
    def retrieve_boba_by_id(boba_id,x):
        #hardcoded list of flavors
        all_flavors = ["cherry","latte","chocolate","chai tea",
        "raspberry", "mango", "neapolitan ice cream", "volcano",
        "strawberry foam cap", "strawberry yogurt","strawberry", "thai tea"
        ]

        prices = {"cherry" : 6.75,"latte": 7,"chocolate": 5.85,"chai tea": 4.95,
        "raspberry": 6.75 , "mango" : 6.75, "neapolitan ice cream": 7.95, "volcano" : 7.95,
        "strawberry foam cap": 8, "strawberry yogurt": 8,"strawberry": 5.85, "thai tea": 5.85}


        if boba_id in all_flavors:
            drink = Boba(prices[boba_id], all_flavors[boba_id])

        else:
            #dunno what to return in this case yet
            drink  = ""

        return drink




## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = MovieClient(os.environ.get("OMDB_API_KEY"))

    movies = client.search("guardians")

    for movie in movies:
        print(movie)

    print(len(movies))
