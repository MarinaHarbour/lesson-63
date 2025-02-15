from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard= True)
button = KeyboardButton(text = "Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
kb.add(button, button2, button3)

inline_kb = InlineKeyboardMarkup(resize_keyboard= True)
button4 = InlineKeyboardButton(text="Рассчитать норму калорий",  callback_data="calories")
button5 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
inline_kb.add(button4, button5)

inline_kb2 = InlineKeyboardMarkup(resize_keyboard = True)

button6 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button7 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button8 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button9 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
inline_kb2.add( button6, button7, button8, button9)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)

@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    await message.answer(f"Название: Product{1} | Описание: описание {1} | Цена: {1 * 100}")
    with open(f"files/1.jpg", "rb") as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product{2} | Описание: описание {2} | Цена: {2 * 100}")
    with open(f"files/2.jpg", "rb") as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product{3} | Описание: описание {3} | Цена: {3 * 100}")
    with open(f"files/3.jpg", "rb") as img:
        await message.answer_photo(img)
    await message.answer(f"Название: Product{4} | Описание: описание {4} | Цена: {4 * 100}")
    with open(f"files/4.jpg", "rb") as img:
        await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_kb2)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()



@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
    await call.answer()

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = int(message.text))
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = int(message.text))
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = int(message.text))

    data = await state.get_data()
    formula = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161
    await message.answer(f"Ваша норма калорий {formula}")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)