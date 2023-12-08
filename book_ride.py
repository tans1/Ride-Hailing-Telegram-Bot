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
from reusable import *

ride_booking_router = Router()

    

@ride_booking_router.message(RideBookingForm.initial)
async def reply(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    await state.update_data(initial={'latitude': latitude, 'longitude': longitude})
    await state.set_state(RideBookingForm.destination)
    await message.answer("📍 Please provide your destination address:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Share Location", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    ))


@ride_booking_router.message(RideBookingForm.destination)
async def reply(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    booking_data = await state.get_data()

    user_id = message.from_user.id
    start_latitude = booking_data['initial']['latitude']
    start_longitude = booking_data['initial']['longitude']
    destination_latitude = latitude
    destination_longitude = longitude

    rideId = bookRide(user_id, start_latitude, start_longitude, destination_latitude, destination_longitude)

    arrivalTime = 20
    await message.answer(
        f"🚗 Your car will arrive after {arrivalTime} minutes. Have a good journey!",
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

    if rideId:
        drivers = getAllDrivers()
        for driver in drivers:
            driver_id = int(driver[1])
            await sendMessagetoUser(driver_id,
                                    "🚗 Someone needs a ride service. Are you ready to accept?",InlineKeyboardMarkup(
                                       inline_keyboard=[[
                                           InlineKeyboardButton(text="✅ Yes, I am ready",callback_data=f'accept_ride {rideId}')]]))

