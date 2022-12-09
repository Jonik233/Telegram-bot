from bot import bot, dp
from keyboards import Buttons
from services import Api
from aiogram import types
from aiogram.dispatcher.filters import Command
import replies

@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=replies.MENU_REPLY, reply_markup=Buttons.MenuBar.menuMarkup)
    await message.delete()
    
@dp.message_handler(Command("movie"))
async def movie_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /movie «movie title»")
    else:
        title = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.MOVIE_REPLY.format(title), reply_markup=Buttons.MarkUp.searchResultsMarkUp(title, "movie"))
        await message.delete()

@dp.message_handler(Command("tv"))
async def tv_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /tv «tv-show»")
    else:
        title = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.TV_REPLY.format(title), reply_markup=Buttons.MarkUp.searchResultsMarkUp(title, "tvSeries"))
        await message.delete()

@dp.message_handler(Command("ratings"))
async def ratings_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=replies.RATINGS_TYPE_REPLY, reply_markup=Buttons.RatingBar.raitingMarkup)
    await message.delete()
    
@dp.callback_query_handler(text_contains='search')
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.SEARCH_REPLY, reply_markup=Buttons.MarkUp.createMarkup([Buttons.homeButton]))
    await callback.message.delete()

@dp.callback_query_handler(text_contains='home')
async def home_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.MENU_REPLY, reply_markup=Buttons.MenuBar.menuMarkup)
    await callback.message.delete()

@dp.callback_query_handler(text_contains='back ')
async def back_callback_handler(callback: types.CallbackQuery):
    
    product_type = callback.data.split()[1]
    title = ' '.join(callback.data.split()[2:])
    text = replies.MOVIE_REPLY.format(title) if product_type == "movie" else replies.TV_REPLY.format(title) 
    
    await callback.message.answer(text=text, reply_markup=Buttons.MarkUp.searchResultsMarkUp(title, product_type))
    await callback.message.delete()
        
@dp.callback_query_handler(text_contains='close')
async def close_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Closing...")
    await callback.message.delete()

@dp.callback_query_handler(text_contains='ratings')
async def films_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.RATINGS_TYPE_REPLY, reply_markup=Buttons.MarkUp.createMarkup([Buttons.generalRaitingButton, Buttons.trendingButton, Buttons.homeButton]))
    await callback.message.delete()
    
@dp.callback_query_handler(text_contains='general_rating')
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=Buttons.MarkUp.createMarkup([Buttons.movieTypeButton, Buttons.tvTypeButton, Buttons.backButton])) 
    await callback.message.delete()

@dp.callback_query_handler(text_contains='trending_rating')
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=Buttons.MarkUp.createMarkup([Buttons.movieTypeButton, Buttons.tvTypeButton, Buttons.backButton])) 
    await callback.message.delete()
    
@dp.callback_query_handler(text_contains='tt')
async def tconstant_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Loading..")
    
    tconst = callback.data.split()[0]
    title = ' '.join(callback.data.split()[1:])
    
    if Api.ApiService.product_is_movie(tconst):
        await callback.message.answer(text=Api.ApiService.movie_model(tconst), reply_markup=Buttons.MarkUp.createMarkup([Buttons.createBackButton(title, "movie")]), parse_mode="HTML")
    elif Api.ApiService.product_is_tvshow(tconst):
        await callback.message.answer(text=Api.ApiService.tv_model(tconst), reply_markup=Buttons.MarkUp.createMarkup([Buttons.createBackButton(title, "tvSeries")]), parse_mode="HTML")
    
    await callback.message.delete()