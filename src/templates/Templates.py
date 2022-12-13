class Template:
    def __init__(self, 
                 title:str=None, 
                 tagline:str=None,
                 summary:str=None, 
                 genres:str=None, 
                 image_url:str=None, 
                 average_rating:float=None,  
                 actors:str=None,  
                 director:str=None,  
                 time_running:int=None, 
                 year_of_exposure:int=None):
                
        self.__title = title
        self.__tagline = tagline
        self.__summary = summary
        self.__genres = genres
        self.__image_url = image_url
        self.__average_rating = average_rating
        self.__actors = actors
        self.__director = director
        self.__time_running = time_running
        self.__year_of_exposure = year_of_exposure
    
    @property
    def title(self):
        if self.__title:
            return self.__title
        return "Undefined"
    
    @property
    def tagline(self):
        if self.__tagline:
            return self.__tagline
        return ""     
    
    @property
    def summary(self):
        if self.__summary:
            return self.__summary
        return "Undefined"
    
    @property
    def genres(self):
        if self.__genres:
            return self.__genres
        return "Undefined"
    
    @property
    def image_url(self):
        if self.__image_url:
            return "http://image.tmdb.org/t/p/w500" + self.__image_url
        return "https://s3picturehouses.s3.eu-central-1.amazonaws.com/header/ph_15578516125cdaeddcb58a7.jpg"
        
    @property
    def average_rating(self):
        if self.__average_rating:
            return self.__average_rating
        return "Undefined rating"
    
    @property
    def actors(self):
        if self.__actors:
            return self.__actors
        return "Undefined"

    @property
    def director(self):
        if self.__director:
            return self.__director
        return "Undefined"
    
    @property
    def time_running(self):
        if self.__time_running:
            return self.__time_running
        return "Undefined time of running"
    
    @property
    def year_of_exposure(self):
        if self.__year_of_exposure:
            return self.__year_of_exposure
        return "Undefined year of exposure"
    
class MovieTemplate(Template):
    
    def __str__(self):
        return f"""
        <b><a href='{str(self.image_url)}'>{self.title}({self.year_of_exposure})</a></b>
<i>{self.tagline}</i>
        \n<b>Genres: </b><a>{', '.join([genre["name"] for genre in self.genres])}</a>
        \n📓{self.summary}
        \n<b>Average rating: </b>\n<a href = '{str(self.image_url)}'>IMDB: </a><b>{self.average_rating}</b>
        \n<b>Main actors: </b>{self.actors}
<b>Director: </b>{self.director}
        \n<b>{self.time_running} min.</b> | <b>{self.year_of_exposure}</b>
        """


class TvTemplate(Template):
    
    def __init__(self, 
                 title:str=None, 
                 tagline:str=None,
                 summary:str=None, 
                 genres:str=None, 
                 image_url:str=None, 
                 average_rating:float=None,  
                 actors:str=None,  
                 seasons:int=None,
                 episodes:int=None,  
                 time_running:int=None, 
                 seriesStartYear:int=None,
                 seriesEndYear:int=None):
        
        super().__init__(title=title, tagline=tagline, summary=summary, genres=genres, image_url=image_url, average_rating=average_rating, actors=actors,time_running=time_running)
        
        self.__seasons = seasons
        self.__episodes = episodes
        self.__seriesStartYear = seriesStartYear
        self.__seriesEndYear = seriesEndYear
    
    @property
    def seasons(self):
        if self.__seasons:
            return self.__seasons
        return "Undefined"
    
    @property
    def episodes(self):
        if self.__episodes:
            return self.__episodes
        return "Undefined"
    
    @property
    def seriesStartYear(self):
        if self.__seriesStartYear:
            return self.__seriesStartYear
        return "Undefined"
    
    @property
    def seriesEndYear(self):
        if self.__seriesEndYear:
            return self.__seriesEndYear
        return "Undefined"
    
    def __str__(self):
        return f"""
        <b><a href='{str(self.image_url)}'>{self.title}({self.seriesStartYear})</a></b>
<i>{self.tagline}</i>
        \n<b>Genres: </b><a>{', '.join([genre["name"] for genre in self.genres])}</a>
        \n📓{self.summary}
        \n<b>Average rating: </b>\n<a href = '{str(self.image_url)}'>IMDB: </a><b>{self.average_rating}</b>
        \n<b>Main actors: </b>{self.actors}
<b>Episodes: </b>{self.episodes}
<b>Seasons: </b>{self.seasons}
        \n<b>{self.time_running} min.</b> | <b>{self.seriesStartYear} - {self.seriesEndYear}</b>
        """