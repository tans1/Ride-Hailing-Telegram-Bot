import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from db import checkUserExists
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from register import *
from login import *
from states import *
from book_ride import *
from rating_review import *

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    if checkUserExists(user_id):
        await message.answer("👋 Welcome back", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Login", callback_data='login'),
                ],
            ]
        ))
    else:
        await message.answer("👋 Welcome to our bot", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Register", callback_data='register'),
                ],
            ]
        ))


@dp.callback_query(lambda callback: callback.data == "register")
async def reply(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationForm.name)
    await callback_query.message.answer("📝 Please enter your name:")


@dp.callback_query(lambda callback: callback.data == "login")
async def reply(callback_query: types.CallbackQuery, state: FSMContext):
    userId = callback_query.from_user.id
    await state.set_state(LoginForm.username)
    await callback_query.message.answer("👤 Please enter your username:")


@dp.message(lambda message: message.text == "Profile Management")
async def process_profile_management(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationForm.name)
    await message.answer("📝 Please enter your name:", reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text == "Ride Booking")
async def process_ride_booking(message: types.Message, state: FSMContext):
    await state.set_state(RideBookingForm.initial)
    await message.answer("🚗 Please share your current location:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Share Location", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    ))
    
@dp.message(lambda message: message.text == "Rating and Reviews")
async def process_ride_booking(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = getUser(user_id)
    if user:
        user_role = user[4]
        await state.set_state(RatingAndReview.rated_person_name)
        if user_role == "driver":
            await message.answer("🚗 Please Provide the passenger name :", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("🚗 Please Provide the driver name :", reply_markup=ReplyKeyboardRemove())


@dp.callback_query(lambda callback: "accept_ride" in callback.data)
async def reply(callback_query: types.CallbackQuery, state: FSMContext):
    rideId = int(callback_query.data.split()[-1])
    driverId = callback_query.from_user.id

    ride = getBookedRide(rideId)
    userId = int(ride[1])
    await bot.send_message(userId,
                           f"🚗 A driver with ID: {driverId} will take you to your destination. "
                           f"If you don't want to proceed, you can cancel your booking.",
                           reply_markup=InlineKeyboardMarkup(
                               inline_keyboard=[[
                                   InlineKeyboardButton(text="🚫 Cancel",
                                                        callback_data=f'cancel_ride {rideId} {driverId}')]]
                           ))


@dp.callback_query(lambda callback: "cancel_ride" in callback.data)
async def reply(callback_query: types.CallbackQuery, state: FSMContext):
    rideId = int(callback_query.data.split()[-2])
    driverId = int(callback_query.data.split()[-1])
    await bot.send_message(driverId, f"🚗 A ride with ID: {rideId} is canceled.")


async def main():
    dp.include_router(register_router)
    dp.include_router(login_router)
    dp.include_router(ride_booking_router)
    dp.include_router(rating_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
