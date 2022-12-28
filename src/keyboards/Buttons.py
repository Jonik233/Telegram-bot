from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import api

search_button = InlineKeyboardButton(text="🔍Search", callback_data="search")
help_button = InlineKeyboardButton(text="🧭Help", callback_data="help")
home_button = InlineKeyboardButton(text="🏠Home", callback_data="home")
close_button = InlineKeyboardButton(text="❌Close", callback_data="close")
back_button = InlineKeyboardButton(text="< Back", callback_data="ratings")
top_rated_films_button = InlineKeyboardButton(text="🎬Top rated products", callback_data = "ratings")
general_raiting_button = InlineKeyboardButton(text="🏆General Rating", callback_data="general")
trending_button = InlineKeyboardButton(text="📈Trending", callback_data="trending")

class MenuBar:    
    menuMarkup = InlineKeyboardMarkup(row_width=2)
    menuMarkup.add(search_button).insert(top_rated_films_button).add(help_button)

class RatingBar: 
    raitingMarkup = InlineKeyboardMarkup(row_width=2)
    raitingMarkup.add(general_raiting_button).insert(trending_button).add(home_button)

class MarkUp:
    
    @staticmethod
    def create_markup(args:list, row_width=2):
        markUp = InlineKeyboardMarkup(row_width=row_width)
        
        for button in args:
            markUp.insert(button)
        
        return markUp
    
    @staticmethod
    def search_results_markup(search_request: str, product_type: str):
        products = api.ApiService.get_products(search_request, product_type)
        searchMarkUp = MarkUp.create_markup([InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="search" + " " + str(product["id"]) + " " + product_type + " " + search_request) for product in products], row_width=1)
        searchMarkUp.add(close_button)
        return searchMarkUp
    
    @staticmethod
    def person_search_markup(search_request: str):
        people = api.ApiService.get_people(search_request)
        name_to_id_list = list()
        
        for person in people:
            actor = api.ApiService.get_person_details(person["id"])
            name_to_id_list.append((actor["id"], actor["name"]))

        buttons = [InlineKeyboardButton(text=name, callback_data=str(id) + " " + search_request + " person") for id, name in name_to_id_list]
       
        searchMarkUp = MarkUp.create_markup(buttons, row_width=1)
        searchMarkUp.add(close_button)

        return searchMarkUp
    
    @staticmethod
    def general_rating_results_markUp(product_type: str):
        
        products = api.ApiService.get_top_rated_movies() if product_type == "movie" else api.ApiService.get_top_rated_tv()

        buttons = [InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="ratings" + " " + str(product["id"]) + " " + product_type + " " + "general") for product in products]
        
        ratingMarkUp = MarkUp.create_markup(buttons, row_width=1)
        ratingMarkUp.add(InlineKeyboardButton(text="< Back", callback_data="general"))
        
        return ratingMarkUp
    
    @staticmethod
    def trending_rating_results_markUp(product_type: str):
        
        products = api.ApiService.get_trending_movies() if product_type == "movie" else api.ApiService.get_trending_tv()

        buttons = [InlineKeyboardButton(text=product["title" if product_type == "movie" else "name"], callback_data="ratings" + " " + str(product["id"]) + " " + product_type + " " + "trending") for product in products]
        
        ratingMarkUp = MarkUp.create_markup(buttons, row_width=1)
        ratingMarkUp.add(InlineKeyboardButton(text="< Back", callback_data="trending"))
        
        return ratingMarkUp
    
class Button:
    
    @staticmethod
    def create_media_search_back_button(callback_data, product_type):
        return InlineKeyboardButton(text="< Back", callback_data=f"back {product_type} {callback_data}")

    @staticmethod
    def create_custom_button(text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)