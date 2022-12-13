from bot import bot, dp
from keyboards import buttons, slider
from services import api
from aiogram import types
from aiogram.dispatcher.filters import Command
import replies


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=replies.MENU_REPLY, reply_markup=buttons.MenuBar.menuMarkup)
    await message.delete()
        
@dp.message_handler(Command("movie"))
async def movie_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /movie «movie title»")
    else:
        title = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.MOVIE_REPLY.format(title), reply_markup=buttons.MarkUp.searchResultsMarkUp(title, "movie"))
        await message.delete()

@dp.message_handler(Command("tv"))
async def tv_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /tv «tv-show»")
    else:
        title = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.TV_REPLY.format(title), reply_markup=buttons.MarkUp.searchResultsMarkUp(title, "tvSeries"))
        await message.delete()

@dp.message_handler(Command("ratings"))
async def ratings_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=replies.RATINGS_TYPE_REPLY, reply_markup=buttons.RatingBar.raitingMarkup)
    await message.delete()
    
@dp.callback_query_handler(text_contains='search')
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.SEARCH_REPLY, reply_markup=buttons.MarkUp.createMarkup([buttons.homeButton]))
    await callback.message.delete()

@dp.callback_query_handler(text_contains='home')
async def home_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.MENU_REPLY, reply_markup=buttons.MenuBar.menuMarkup)
    await callback.message.delete()

@dp.callback_query_handler(text_contains='back ')
async def back_callback_handler(callback: types.CallbackQuery):
    
    product_type = callback.data.split()[1]
    title = ' '.join(callback.data.split()[2:])
    text = replies.MOVIE_REPLY.format(title) if product_type == "movie" else replies.TV_REPLY.format(title) 
    
    await callback.message.answer(text=text, reply_markup=buttons.MarkUp.searchResultsMarkUp(title, product_type))
    await callback.message.delete()
        
@dp.callback_query_handler(text='close')
async def close_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Closing...")
    await callback.message.delete()

@dp.callback_query_handler(text='ratings')
async def films_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.RATINGS_TYPE_REPLY, reply_markup=buttons.MarkUp.createMarkup([buttons.generalRaitingButton, buttons.trendingButton, buttons.homeButton]))
    await callback.message.delete()

@dp.callback_query_handler(text="general")
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=buttons.MarkUp.createMarkup([buttons.Button.createCustomButton("Movies", "movie_general"), buttons.Button.createCustomButton("TV-Series", "tv_general"), buttons.backButton])) 
    await callback.message.delete()

@dp.callback_query_handler(text='trending')
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=buttons.MarkUp.createMarkup([buttons.Button.createCustomButton("Movies", "movie_trending"), buttons.Button.createCustomButton("TV-Series", "tv_trending"), buttons.backButton])) 
    await callback.message.delete()

@dp.callback_query_handler(text='movie_general')
async def movie_general_rating_handler(callback: types.CallbackQuery):
    slider.Slider.data = api.ApiService.get_top_rated_movies()
    await callback.message.answer(text="🏆Top rated movies", reply_markup=slider.Slider.get_current_page())
    await callback.message.delete()

@dp.callback_query_handler(text='movie_trending')
async def movie_trending_rating_handler(callback: types.CallbackQuery):
    pass

@dp.callback_query_handler(text='tv_general')
async def tv_general_rating_hendler(callback: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="tv_trending")
async def tv_trending_rating_handler(callback: types.CallbackQuery):
    pass

@dp.callback_query_handler(text="left")
async def go_left_handler(callback: types.CallbackQuery):
    if slider.Slider.go_left():
        await callback.message.edit_reply_markup(slider.Slider.go_left())
    else:
        await callback.answer("You can't go left")

@dp.callback_query_handler(text="right")
async def go_left_handler(callback: types.CallbackQuery):
    if slider.Slider.go_right():
        await callback.message.edit_reply_markup(slider.Slider.go_right())
    else:
        await callback.answer("You can't go right")
    
@dp.callback_query_handler(text_contains='tt')
async def tconstant_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Loading..")
    
    tconst = callback.data.split()[0]
    title = ' '.join(callback.data.split()[1:])
    
    if api.ApiService.product_is_movie(tconst):
        await callback.message.answer(text=api.ApiService.movie_model(tconst), reply_markup=buttons.MarkUp.createMarkup([buttons.Button.createBackButton(title, "movie")]), parse_mode="HTML")
    elif api.ApiService.product_is_tvshow(tconst):
        await callback.message.answer(text=api.ApiService.tv_model(tconst), reply_markup=buttons.MarkUp.createMarkup([buttons.Button.createBackButton(title, "tvSeries")]), parse_mode="HTML")
    
    await callback.message.delete()