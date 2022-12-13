import requests
from templates import templates

class ApiService:  
    
    #urls   
    __movie_search_url = "https://api.themoviedb.org/3/search/movie?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US&page=1&include_adult=false&query={0}"
    
    __movie_details_url = "https://api.themoviedb.org/3/movie/{0}?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US"
    
    __movie_credits_url = "https://api.themoviedb.org/3/movie/{0}/credits?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US"
    
    __tv_search_url = "https://api.themoviedb.org/3/search/tv?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US&page=1&include_adult=false&query={0}"
    
    __tv_details_url = "https://api.themoviedb.org/3/tv/{0}?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US"
    
    __tv_credits_url = "https://api.themoviedb.org/3/tv/{0}/aggregate_credits?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US"
        
    __top_rated_movies_url = "https://api.themoviedb.org/3/movie/top_rated?api_key=15e383204c1b8a09dbfaaa4c01ed7e17&language=en-US&page=1"
    
    @classmethod
    def get_products(cls, search_request, product_type):
        
        url = cls.__movie_search_url.format(search_request) if product_type == "movie" else cls.__tv_search_url.format(search_request)
        
        response = requests.request("GET", url).json()
        results = response["results"]
        
        return results

    @classmethod
    def get_movie_details(cls, id):

        url = cls.__movie_details_url.format(id)
        
        response = requests.request("GET", url)
        
        return response.json()
    
    @classmethod
    def get_movie_credits(cls, id):
        
        url = cls.__movie_credits_url.format(id)
        
        response = requests.request("GET", url).json()
        
        return response
    
    @classmethod
    def get_tv_details(cls, id):
        
        url = cls.__tv_details_url.format(id)
        
        response = requests.request("GET", url).json()
        
        return response
    
    @classmethod
    def get_tv_credits(cls, id):
        
        url = cls.__tv_credits_url.format(id)
        
        response = requests.request("GET", url).json()
        
        return response
    
    @classmethod
    def movie_model(cls, id):
        movie_details = cls.get_movie_details(id)
        template = templates.MovieTemplate(title=movie_details["title"], 
                                        summary=movie_details["overview"],
                                        tagline=movie_details["tagline"],
                                        genres=movie_details["genres"],
                                        image_url=movie_details["poster_path"],
                                        average_rating=movie_details["vote_average"],
                                        actors=cls.get_actors(id, "movie"),
                                        director=cls.get_movie_director(id),
                                        time_running=movie_details["runtime"],
                                        year_of_exposure=movie_details["release_date"].split("-")[0])
        
        return str(template)
    
    @classmethod
    def tv_model(cls, id):
        tv_details = cls.get_tv_details(id)
        template = templates.TvTemplate(title=tv_details["original_name"],
                                           summary=tv_details["overview"], 
                                           tagline=tv_details["tagline"],
                                           genres=tv_details["genres"],
                                           image_url=tv_details["poster_path"], 
                                           average_rating=tv_details["vote_average"],
                                           actors=cls.get_actors(id, "tv"),
                                           seasons=tv_details["number_of_seasons"], 
                                           episodes=tv_details["number_of_episodes"], 
                                           time_running=tv_details["episode_run_time"][0] if len(tv_details["episode_run_time"]) != 0 else "∞",
                                           seriesStartYear=tv_details["first_air_date"].split("-")[0],
                                           seriesEndYear=tv_details["last_air_date"].split("-")[0]
                                           )
        return str(template)
        
    @classmethod
    def get_actors(cls, id, product_type):
 
        cast = cls.get_movie_credits(id)["cast"] if product_type == "movie" else cls.get_tv_credits(id)["cast"]
        
        if len(cast) != 0:
            actors = ", ".join(actor["name"] for actor in cast[:2])
            return actors
        
        return None
    
    @classmethod
    def get_movie_director(cls, id):
        
        cast = cls.get_movie_credits(id)["crew"]
        
        if len(cast) != 0:
            for person in cast:
                keys = person.keys()
                if keys.__contains__("job") and person["job"] == "Director":
                    return person["name"]
        
        return None
    
    @classmethod
    def get_top_rated_movies(cls):
        
        url = cls.__top_rated_movies_url
        
        response = requests.request("GET", url).json()
        
        return response