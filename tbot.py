from distutils.command.build import build
from aiogram import Dispatcher, executor, types, Bot
from black import out
from main import get_weather
import aiogram.utils.markdown as fmt
import os, shutil
from dotenv import load_dotenv
import requests
from datetime import datetime


load_dotenv()

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


@dp.message_handler(commands='charts')
async def charts(message: types.Message):
    chat_id = message.chat.id
    path = f'.\\data\{str(chat_id)}'
    os.makedirs(path, exist_ok=True)
    output_dir = path

    urls = [
    'https://www.aviationweather.gov/data/iffdp/2722.pdf',
    'https://www.aviationweather.gov/data/iffdp/2723.pdf',
    'https://www.aviationweather.gov/data/iffdp/2724.pdf',
    'https://www.aviationweather.gov/data/iffdp/2103.pdf'
    ]
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    for url in urls:
    	with requests.Session() as s:
    		response = s.get(url, headers=headers)
    		if response.status_code == 200:
    			file_path = os.path.join(output_dir, os.path.basename(url))
    			with open(file_path, 'wb') as f:
    				f.write(response.content)

    for file in os.listdir(output_dir):
    	file_path = os.path.join(output_dir, file)
    	await bot.send_document(chat_id, document=open(file_path, 'rb'))

    	try:
    		if os.path.isfile(file_path) or os.path.islink(file_path):
    			os.unlink(file_path)
    		elif os.path.isdir(file_path):
    			shutil.rmtree(file_path)
    	except Exception as e:
    		print('Failed to delete %s. Reason: %s' % (file_path, e))	

if __name__ == '__main__':
    executor.start_polling(dp)