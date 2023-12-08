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
from states import *
import reusable

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
   InlineKeyboardMarkup,
   InlineKeyboardButton
)


    
rating_router = Router()

@rating_router.message(RatingAndReview.rated_person_name)
async def reply(message: Message, state: FSMContext):
    await state.update_data(rated_person_name = message.text)
    
    await state.set_state(RatingAndReview.rating)
    await message.answer(
        "Please provide how much rate the person out of 10 :- ",
        reply_markup=ReplyKeyboardRemove()
    )
@rating_router.message(RatingAndReview.rating)
async def reply(message: Message, state: FSMContext):
    await state.update_data(rating = message.text)
    await state.set_state(RatingAndReview.review)
    await message.answer(
        "Please provide your review opinion :- ",
        reply_markup=ReplyKeyboardRemove())

@rating_router.message(RatingAndReview.review)
async def process_role(message: types.Message, state: FSMContext):
    await state.update_data(review = message.text) 
    data = await state.get_data()
    name = data['rated_person_name']
    rating = data['rating']
    review = data['review']
    user = getUserbyName(name)
    if user:
        await reusable.sendMessagetoUser(int(user[1]), "🌟📬 Exciting News! 🌟📬",ReplyKeyboardRemove())
        await reusable.sendMessagetoUser(int(user[1]), f"🎉 Your Rating: {rating}/10 🌟",ReplyKeyboardRemove())
        await reusable.sendMessagetoUser(int(user[1]), f"📝 Your Review: {review} 🚀",ReplyKeyboardMarkup(
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
        ))


    
    await message.answer(
        "Thanks for your feedback,",
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


