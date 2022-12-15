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

    #IDKNO WHAT X IS, IT SAID I WAS SENDING TWO THINGS HERE LMAO BUT IT WORKS BRO
    def retrieve_boba_by_id(x,boba_id):
        #hardcoded list of flavors
        all_flavors = ["cherry","latte","chocolate","chai tea",
        "raspberry", "mango", "neapolitan ice cream", "volcano",
        "strawberry foam cap", "strawberry yogurt","strawberry", "thai tea"
        ]

        prices = {"cherry" : 6.75,"latte": 7,"chocolate": 5.85,"chai tea": 4.95,
        "raspberry": 6.75 , "mango" : 6.75, "neapolitan ice cream": 7.95, "volcano" : 7.95,
        "strawberry foam cap": 8, "strawberry yogurt": 8,"strawberry": 5.85, "thai tea": 5.85}


        if boba_id in all_flavors:
            drink = Boba(prices[boba_id], boba_id)

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
