from bot import bot, dp
from keyboards import buttons
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
        await bot.send_message(chat_id=message.from_user.id, text=replies.MOVIE_REPLY.format(title), reply_markup=buttons.MarkUp.search_results_markup(title, "movie"))
        await message.delete()

@dp.message_handler(Command("tv"))
async def tv_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /tv «tv-show»")
    else:
        title = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.TV_REPLY.format(title), reply_markup=buttons.MarkUp.search_results_markup(title, "tvSeries"))
        await message.delete()
    
@dp.message_handler(Command("person"))
async def person_handler(message: types.Message):
    if len(message.text.split()) == 1:
        await bot.send_message(chat_id=message.from_user.id, text="Usage: /person «name»")
    else:
        name = " ".join(message.text.split()[1:])
        await bot.send_message(chat_id=message.from_user.id, text=replies.PERSON_REPLY.format(name), reply_markup=buttons.MarkUp.person_search_markup(name))
        await message.delete()
        
@dp.message_handler(Command("ratings"))
async def ratings_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=replies.RATINGS_TYPE_REPLY, reply_markup=buttons.RatingBar.raitingMarkup)
    await message.delete()

@dp.callback_query_handler(text="help")
async def help_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.HELP_REPLY, reply_markup=buttons.MarkUp.create_markup([buttons.home_button]))
    await callback.message.delete()
    
@dp.callback_query_handler(text='search')
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.SEARCH_REPLY, reply_markup=buttons.MarkUp.create_markup([buttons.home_button]))
    await callback.message.delete()

@dp.callback_query_handler(text='home')
async def home_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.MENU_REPLY, reply_markup=buttons.MenuBar.menuMarkup)
    await callback.message.delete()

@dp.callback_query_handler(text_contains='back ')
async def back_callback_handler(callback: types.CallbackQuery):
    
    product_type = callback.data.split()[1]
    title = ' '.join(callback.data.split()[2:])
    text = replies.MOVIE_REPLY.format(title) if product_type == "movie" else replies.TV_REPLY.format(title) 
    
    await callback.message.answer(text=text, reply_markup=buttons.MarkUp.search_results_markup(title, product_type))
    await callback.message.delete()
        
@dp.callback_query_handler(text='close')
async def close_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Closing...")
    await callback.message.delete()

@dp.callback_query_handler(text='ratings')
async def films_callback_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.RATINGS_TYPE_REPLY, reply_markup=buttons.MarkUp.create_markup([buttons.general_raiting_button, buttons.trending_button, buttons.home_button]))
    await callback.message.delete()

@dp.callback_query_handler(text="general")
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("Movies", "movie_general"), buttons.Button.create_custom_button("TV-Series", "tv_general"), buttons.back_button])) 
    await callback.message.delete()

@dp.callback_query_handler(text='trending')
async def movie_rate_handler(callback: types.CallbackQuery):
    await callback.message.answer(text=replies.PRODUCT_TYPE_REPLY, reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("Movies", "movie_trending"), buttons.Button.create_custom_button("TV-Series", "tv_trending"), buttons.back_button])) 
    await callback.message.delete()

@dp.callback_query_handler(text='movie_general')
async def movie_general_rating_handler(callback: types.CallbackQuery):
    await callback.message.answer(text="🏆Top rated movies", reply_markup=buttons.MarkUp.general_rating_results_markUp("movie"))
    await callback.message.delete()

@dp.callback_query_handler(text='movie_trending')
async def movie_trending_rating_handler(callback: types.CallbackQuery):
    await callback.message.answer(text="📈Trending movies", reply_markup=buttons.MarkUp.trending_rating_results_markUp("movie"))
    await callback.message.delete()
    
@dp.callback_query_handler(text='tv_general')
async def tv_general_rating_hendler(callback: types.CallbackQuery):
    await callback.message.answer(text="🏆Top rated tv-series", reply_markup=buttons.MarkUp.general_rating_results_markUp("tvSeries"))
    await callback.message.delete()

@dp.callback_query_handler(text="tv_trending")
async def tv_trending_rating_handler(callback: types.CallbackQuery):
    await callback.message.answer(text="📈Trending tv-series", reply_markup=buttons.MarkUp.trending_rating_results_markUp("tvSeries"))
    await callback.message.delete()
    
@dp.callback_query_handler(text_contains='search ')
async def search_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Loading..")
    
    data = callback.data.split()
    id = data[1]
    product_type = data[2]
    title = ' '.join(data[3:])
        
    if product_type == "movie":
        await callback.message.answer(text=api.ApiService.movie_model(id), reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_media_search_back_button(title, product_type)]), parse_mode="HTML")
    else:
        await callback.message.answer(text=api.ApiService.tv_model(id), reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_media_search_back_button(title, product_type)]), parse_mode="HTML") 
         
    await callback.message.delete()
    
@dp.callback_query_handler(text_contains='ratings ')
async def ratings_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Loading..")
    
    data = callback.data.split()
    id = data[1]
    product_type = data[2]
    rating_type = data[3]
    
    if product_type == "movie" and rating_type == "general":
        await callback.message.answer(text=api.ApiService.movie_model(id), 
                                      reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("< Back", "movie_general")], row_width=1), parse_mode="HTML")
   
    elif product_type == "movie" and rating_type == "trending":
        await callback.message.answer(text=api.ApiService.movie_model(id), reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("< Back", "movie_trending")], row_width=1), parse_mode="HTML")
   
    elif product_type == "tvSeries" and rating_type == "general":
        await callback.message.answer(text=api.ApiService.tv_model(id), 
                                      reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("< Back", "tv_general")], row_width=1), parse_mode="HTML")
    else:
        await callback.message.answer(text=api.ApiService.tv_model(id),
                                      reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("< Back", "tv_trending")], row_width=1), parse_mode="HTML")
    
    await callback.message.delete()
    
@dp.callback_query_handler(text_contains=' person')
async def person_callback_handler(callback: types.CallbackQuery):
    await callback.answer("Loading..")
    
    data = callback.data.split()
    id = data[0]
    search_request = " ".join(data[1:len(data) - 1])
    
    await callback.message.answer(text=api.ApiService.person_model(id),
                                  reply_markup=buttons.MarkUp.create_markup([buttons.Button.create_custom_button("< Back", "person_list " + search_request)], row_width=1), parse_mode="HTML")
   
    await callback.message.delete()

@dp.callback_query_handler(text_contains='person_list ')
async def person_back_button_handler(callback: types.CallbackQuery):
    
    search_request = ' '.join(callback.data.split()[1:])
    await callback.message.answer(text=replies.PERSON_REPLY.format(search_request), reply_markup=buttons.MarkUp.person_search_markup(search_request))
    await callback.message.delete()