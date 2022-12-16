from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import api

searchButton = InlineKeyboardButton(text="🔍Search", callback_data="search")
helpButton = InlineKeyboardButton(text="🧭Help", callback_data="help")
homeButton = InlineKeyboardButton(text="🏠Home", callback_data="home")
closeButton = InlineKeyboardButton(text="❌Close", callback_data="close")
backButton = InlineKeyboardButton(text="< Back", callback_data="ratings")
topRatedFilms = InlineKeyboardButton(text="🎬Top rated products", callback_data = "ratings")
generalRaitingButton = InlineKeyboardButton(text="🏆General Rating", callback_data="general")
trendingButton = InlineKeyboardButton(text="📈Trending", callback_data="trending")
left_button = InlineKeyboardButton(text="<<", callback_data="left")
right_button = InlineKeyboardButton(text=">>", callback_data="right")

class MenuBar:    
    menuMarkup = InlineKeyboardMarkup(row_width=2)
    menuMarkup.add(searchButton).insert(topRatedFilms).add(helpButton)

class RatingBar: 
    raitingMarkup = InlineKeyboardMarkup(row_width=2)
    raitingMarkup.add(generalRaitingButton).insert(trendingButton).add(homeButton)

class MarkUp:
    
    @staticmethod
    def createMarkup(args:list, row_width=2):
        markUp = InlineKeyboardMarkup(row_width=row_width)
        
        for button in args:
            markUp.insert(button)
        
        return markUp
    
    @staticmethod
    def searchResultsMarkUp(search_request: str, product_type: str):
        products = api.ApiService.get_products(search_request, product_type)
        searchMarkUp = MarkUp.createMarkup([InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="search" + " " + str(product["id"]) + " " + product_type + " " + search_request) for product in products], row_width=1)
        searchMarkUp.add(closeButton)
        return searchMarkUp
    
    @staticmethod
    def personSearchMarkUp(search_request: str):
        people = api.ApiService.get_people(search_request)
        name_to_id_list = list()
        
        for person in people:
            actor = api.ApiService.get_person_details(person["id"])
            name_to_id_list.append((actor["id"], actor["name"]))

        searchMarkUp = MarkUp.createMarkup([InlineKeyboardButton(text=name, callback_data=str(id) + " " + search_request + " person") for id, name in name_to_id_list], row_width=1)
        searchMarkUp.add(closeButton)

        return searchMarkUp
    
    @staticmethod
    def generalRatingResultsMarkUp(product_type: str):
        
        products = api.ApiService.get_top_rated_movies() if product_type == "movie" else api.ApiService.get_top_rated_tv()

        ratingMarkUp = MarkUp.createMarkup([InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="ratings" + " " + str(product["id"]) + " " + product_type + " " + "general") for product in products], row_width=1)
        ratingMarkUp.add(InlineKeyboardButton(text="< Back", callback_data="general"))
        
        return ratingMarkUp
    
    @staticmethod
    def trendingRatingResultsMarkUp(product_type: str):
        
        products = api.ApiService.get_trending_movies() if product_type == "movie" else api.ApiService.get_trending_tv()

        ratingMarkUp = MarkUp.createMarkup([InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="ratings" + " " + str(product["id"]) + " " + product_type + " " + "trending") for product in products], row_width=1)
        ratingMarkUp.add(InlineKeyboardButton(text="< Back", callback_data="trending"))
        
        return ratingMarkUp
    
class Button:
    
    @staticmethod
    def createMediaSearchBackButton(callback_data, product_type):
        return InlineKeyboardButton(text="< Back", callback_data=f"back {product_type} {callback_data}")

    @staticmethod
    def createCustomButton(text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)