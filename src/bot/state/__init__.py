from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    waiting_for_title = State()
    waiting_for_poster = State()
    waiting_for_price = State()
    waiting_for_description = State()
    waiting_for_count = State()
    
class Update(StatesGroup):
    waiting_for_new_title = State()
    waiting_for_new_price = State()
    waiting_for_new_count = State()
    waiting_for_new_description = State()
    waiting_for_new_poster = State()