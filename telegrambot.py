from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7982861761:AAFuXa_bOkC4BBTUgFI-LToqpmchA_mxVUk'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]],
    resize_keyboard=True)


inline_choices = InlineKeyboardMarkup()
bt = InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')
bt2 = InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas')
inline_choices.row(bt, bt2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Привет')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий Вашему здоровью.\n'
                         f'Чтобы начать, нажмите "Рассчитать"', reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = inline_choices)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Калории = 10 * вес + 6.25 * рост - 5 * возраст - 161')



@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    norma = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()
    global a
    global g
    global w
    global n
    a = age
    g = growth
    w = weight
    n = norma

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(f'Ваш возраст:  {a}\nВаш рост:      {g} \nВаш вес:          {w}\n'
                             f'Ваша норма калорий: {n}')
    await state.finish()
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

