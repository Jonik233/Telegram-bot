class Parser:
    
    @staticmethod
    def parse_title(product:dict):
        if isinstance(product, dict):
            keys = [*product.keys()]
            
            if keys.__contains__("title"):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("title"):
                    return title_data["title"]
                
        return None
    
    @staticmethod
    def parse_summary(product:dict):
        if isinstance(product, dict):
            keys = [*product.keys()]
            
            if keys.__contains__("plotSummary"):
                summary_data = product["plotSummary"]
                summary_keys = [*summary_data.keys()]
                
                if summary_keys.__contains__("text"):
                    return summary_data["text"]
                
        return None
            
    
    @staticmethod
    def parse_genres(product:dict):
        if isinstance(product, dict):
            keys = [*product.keys()]
            
            if keys.__contains__("genres"):
                return product["genres"]
        
        return None
    
    @staticmethod
    def parse_image_url(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                keys = [*title_data.keys()]
                
                if keys.__contains__("image"):
                    image_data = title_data["image"]
                    image_keys = [*image_data.keys()]
                    
                    if image_keys.__contains__("url"):
                        return image_data["url"]
        
        return None
    
    @staticmethod
    def parse_average_rating(product:dict):
        if isinstance(product, dict):
            keys = [*product.keys()]
            
            if keys.__contains__("ratings"):
                ratings_data = product["ratings"]
                ratings_keys = [*ratings_data.keys()] 
                
                if ratings_keys.__contains__("rating"):
                    return ratings_data["rating"]   
        
        return None
                
    
    @staticmethod
    def parse_time_ranning(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("runningTimeInMinutes"):
                    return title_data["runningTimeInMinutes"]
        
        return None
    
    @staticmethod
    def parse_year_of_exposure(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("year"):
                    return title_data["year"]
        
        return None
    
    @staticmethod
    def parse_series_start_year(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("seriesStartYear"):
                    return title_data["seriesStartYear"]
        
        return None
    
    @staticmethod
    def parse_series_end_year(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("seriesEndYear"):
                    return title_data["seriesEndYear"]
        
        return None
    
    @staticmethod
    def parse_episodes(product:dict):
        if isinstance(product, dict):
            
            if Parser.parse_title(product):
                title_data = product["title"]
                title_keys = [*title_data.keys()]
                
                if title_keys.__contains__("numberOfEpisodes"):
                    return title_data["numberOfEpisodes"]
        
        return None
    