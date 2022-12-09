from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import Api

searchButton = InlineKeyboardButton(text="🔍Search", callback_data="search")
helpButton = InlineKeyboardButton(text="🧭Help", callback_data="help")
homeButton = InlineKeyboardButton(text="🏠Home", callback_data="home")
closeButton = InlineKeyboardButton(text="❌Close", callback_data="close")
backButton = InlineKeyboardButton(text="< Back", callback_data="ratings")
topRatedFilms = InlineKeyboardButton(text="🎬Top rated products", callback_data = "ratings")
movieTypeButton = InlineKeyboardButton(text="Movie", callback_data = "movie_rate")
tvTypeButton = InlineKeyboardButton(text="TV-Series", callback_data = "tv_rate")
generalRaitingButton = InlineKeyboardButton(text="🏆General Rating", callback_data="general_rating")
trendingButton = InlineKeyboardButton(text="📈Trending", callback_data="trending_rating")

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
        products = Api.ApiService.get_products(search_request, product_type)
        searchMarkUp = MarkUp.createMarkup([InlineKeyboardButton(text=product["l"], callback_data=product["id"] + " " + search_request) for product in products], row_width=1)
        searchMarkUp.add(closeButton)
        return searchMarkUp


def createBackButton(callback_data, product_type):
    return InlineKeyboardButton(text="< Back", callback_data=f"back {product_type} {callback_data}")