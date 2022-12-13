import requests
from templates import Templates
from .data_parser import Parser

class ApiService:
    #url that leads to a complete list of movies that are relevant to a particular search request
    __general_url = "https://imdb8.p.rapidapi.com/auto-complete"
    
    #url that leads to a specific movie which is requested by a particular tconstant
    __specific_movie_url = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    
    #url that leads to a specif list of crew members which is requested by a particular tconstant
    __crew_url = "https://imdb8.p.rapidapi.com/title/get-top-crew"
    
    #url that leads to top rated movies
    __top_rated_movies_url = "https://online-movie-database.p.rapidapi.com/title/get-top-rated-movies"
    
    #query which is used for general search request(general_url) 
    __general_querystring = {"q":""}
    
    #query which is used for specific requests(specific_movie_url, crew_url)
    __specific_querystring = {"tconst":"","currentCountry":"US"}
    
    #RapidApi headers
    __headers = {
        "X-RapidAPI-Key": "e93353dad1msh2f0b276cbf2c4d8p19e880jsnec75409e79e0",
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }
    
    @classmethod
    def get_products(cls, search_request, product_type):
        
        cls.__general_querystring["q"] = search_request
        
        response = requests.request("GET", cls.__general_url, headers=cls.__headers, params=cls.__general_querystring)
        
        products = response.json()["d"]
        
        filtered_products = []
        
        for product in products:
            keys = [*product.keys()]
            if keys.__contains__("qid"):
                if product["qid"] == product_type:
                    filtered_products.append(product)
        
        return filtered_products
    
    @classmethod
    def get_product(cls, tconst):
        
        cls.__specific_querystring["tconst"] = tconst
        
        response = requests.request("GET", cls.__specific_movie_url, headers=cls.__headers, params=cls.__specific_querystring)
        
        return response.json()
    
    @classmethod
    def movie_model(cls, tconstant):
        movie_info = cls.get_product(tconstant)
        template = Templates.MovieTemplate(title=Parser.parse_title(movie_info), 
                                        summary=Parser.parse_summary(movie_info),
                                        genres=Parser.parse_genres(movie_info),
                                        image_url=Parser.parse_image_url(movie_info),
                                        average_rating=Parser.parse_average_rating(movie_info),
                                        actors=cls.get_actors(tconstant),
                                        director=cls.get_movie_director(tconstant),
                                        time_running=Parser.parse_time_ranning(movie_info),
                                        year_of_exposure=Parser.parse_year_of_exposure(movie_info))
        return str(template)

    @classmethod
    def tv_model(cls, tconstant):
        tv_info = cls.get_product(tconstant)
        template = Templates.TvTemplate(title=Parser.parse_title(tv_info), 
                                        summary=Parser.parse_summary(tv_info),
                                        genres=Parser.parse_genres(tv_info),
                                        image_url=Parser.parse_image_url(tv_info),
                                        average_rating=Parser.parse_average_rating(tv_info),
                                        actors=cls.get_actors(tconstant),
                                        episodes=Parser.parse_episodes(tv_info),
                                        time_running=Parser.parse_time_ranning(tv_info),
                                        seriesStartYear=Parser.parse_series_start_year(tv_info),
                                        seriesEndYear=Parser.parse_series_end_year(tv_info))
        
        return str(template)

    @classmethod
    def get_actors(cls, tconst):
        
        cls.__specific_querystring["tconst"] = tconst
        
        response1 = requests.request("GET", cls.__specific_movie_url, headers=cls.__headers, params=cls.__specific_querystring).json()
        
        if Parser.parse_title(response1):
        
            title = response1["title"]["title"]
        
            cls.__general_querystring["q"] = title
            response2 = requests.request("GET", cls.__general_url, headers=cls.__headers, params=cls.__general_querystring)
            movies = response2.json()["d"]
            
            for movie in movies:
                if movie["id"] == tconst:
                    keys = [*movie.keys()] 
                    if keys.__contains__("s"):
                        return movie["s"]
            
        return None
        
    @classmethod
    def get_movie_director(cls, tconst):
        
        cls.__specific_querystring["tconst"] = tconst
        
        response = requests.request("GET", cls.__crew_url, headers=cls.__headers, params=cls.__specific_querystring).json()
        keys = [*response.keys()]
        
        if keys.__contains__("directors"):
            data = response["directors"]
            
            if len(data) != 0:
                data_keys = [*data[0].keys()]
                
                if data_keys.__contains__("name"):
                    return data[0]["name"]
        
        return None
    
    @classmethod
    def get_top_rated_movies(cls):
        
        response = requests.request("GET", cls.__top_rated_movies_url, headers=cls.__headers).json()[:30]
        results = []
        
        for result in response:
            results.append(result["id"].split("/")[2])
        
        return results

    @classmethod
    def product_is_movie(cls, tconst):
        
        product = cls.get_product(tconst)
        
        if product["title"]["titleType"] == "movie":
            return True
        
        return False
    
    @classmethod
    def product_is_tvshow(cls, tconst):
        
        product = cls.get_product(tconst)
        
        if product["title"]["titleType"] == "tvSeries":
            return True
        
        return False
    