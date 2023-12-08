from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    name = State()
    phone_number = State()
    role = State()
    username = State()
    password = State()
    
    
class RideBookingForm(StatesGroup):
    initial = State()
    destination = State()
    
    
    
class LoginForm(StatesGroup):
    username = State()
    password = State()

class RatingAndReview(StatesGroup):
    rated_person_name = State()
    rating =  State()
    review = State()
    