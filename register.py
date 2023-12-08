import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import *
from states import RegistrationForm

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
   InlineKeyboardMarkup,
   InlineKeyboardButton
)


    
register_router = Router()

@register_router.message(RegistrationForm.name)
async def reply(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    
    await state.set_state(RegistrationForm.phone_number)
    await message.answer(
        "Share your phone number :- ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="phone number", request_contact = True),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard = True
        ),
    )
@register_router.message(RegistrationForm.phone_number)
async def reply(message: Message, state: FSMContext):
    await state.update_data(phone_number = message.contact.phone_number)
    await state.set_state(RegistrationForm.role)
    await message.answer(
        "Role :- ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Driver"),
                    KeyboardButton(text="Passenger"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard = True
        ),
    )

@register_router.message(RegistrationForm.role)
async def process_role(message: types.Message, state: FSMContext):
    await state.update_data(role=message.text.lower())

    await state.set_state(RegistrationForm.username)
    await message.answer("Username :- ", reply_markup = ReplyKeyboardRemove())  
    
@register_router.message(RegistrationForm.username)
async def reply(message: Message, state: FSMContext):
    await state.update_data(username = message.text)
    
    await state.set_state(RegistrationForm.password)
    await message.answer("Password", reply_markup = ReplyKeyboardRemove())  
    
@register_router.message(RegistrationForm.password)
async def reply(message: Message, state: FSMContext):
    await state.update_data(password = message.text) 
    user_data = await state.get_data()
    user_id = message.from_user.id
    if checkUserExists(user_id):
        updateUserData(
            user_id,user_data['name'], 
            user_data['phone_number'],user_data['role'], 
            user_data['username'],user_data['password'])
        
    else:   
        createUser(
            user_id,user_data['name'], 
            user_data['phone_number'],user_data['role'], 
            user_data['username'],user_data['password']
            )
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


