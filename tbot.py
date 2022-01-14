from aiogram import Dispatcher, executor, types, Bot
from main import get_weather
import aiogram.utils.markdown as fmt
import os
#from dotenv import load_dotenv

#load_dotenv()

token = os.getenv("TELEGRAM_TEST_TOKEN") 

bot = Bot(token=token)

dp = Dispatcher(bot)


print('Telegram BOT connected')
print('======================')

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Ready to work!')


@dp.message_handler(commands='help')
async def help(message: types.Message):
	await message.reply(
		fmt.text(
			fmt.text('Available commands'),
			fmt.text('/metar (/m) ____ - METAR for airport'),
			fmt.text('/taf (/t) ____ - Full forecast for airport'),
			fmt.text('/fa) ____ - Area weather forecast in GAMET format (RUSSIA only)'),
            fmt.text('Also available in Discord:'),
			fmt.text('http://tiny.cc/znjluz'),
			sep='\n'
		), parse_mode="HTML"
	)


@dp.message_handler(commands=['metar', 'm', 'sa'])
async def metar(message: types.Message):
	airport = message.get_args()
	await message.answer(get_weather('METAR', airport))
		

@dp.message_handler(commands=['taf', 't'])
async def taf(message: types.Message):
	airport = message.get_args()
	await message.answer(get_weather('TAF', airport))


@dp.message_handler(commands='fa')
async def fa(message: types.Message):
	airport = message.get_args()
	await message.answer(get_weather('FA', airport))
		

if __name__ == '__main__':
    executor.start_polling(dp)