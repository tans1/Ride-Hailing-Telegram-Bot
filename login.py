from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import *
from states import *
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
   InlineKeyboardMarkup,
   InlineKeyboardButton
)

login_router = Router()



    
    
@login_router.message(LoginForm.username)
async def reply(message: Message, state: FSMContext):
    await state.update_data(username = message.text)
    
    await state.set_state(LoginForm.password)
    await message.answer("Password", reply_markup = ReplyKeyboardRemove())  
    
@login_router.message(LoginForm.password)
async def reply(message: Message, state: FSMContext):
    await state.update_data(password = message.text) 
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    if loginUser(user_data['username'], user_data['password']):
         await message.answer(
            "Please use the following keyboard buttons",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Profile Management"),
                        KeyboardButton(text="Ride Booking")
                    ],
                    [
                        KeyboardButton(text="Rating and Reviews"),
                        KeyboardButton(text="View History"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:   
        await message.answer("Invalid Credential, try again",reply_markup = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="login", callback_data='login'),
            ],]))