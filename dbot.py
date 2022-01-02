import discord
from discord.ext.commands import Bot
from main import get_weather
import os
from dotenv import load_dotenv

load_dotenv()

PREFIX = '.'

client = Bot(command_prefix=PREFIX)
client.remove_command('help')


@client.event

async def on_ready():
	print('Discord BOT connected')
	print('=====================')
	await client.change_presence(activity=discord.Game(name=".help for help!"))


@client.command(name='t', aliases= ['taf'],pass_context=True)
@client.event
async def t(ctx, airport):
#taf
	# author = ctx.message.author
	await ctx.send(get_weather('taf', airport))


@client.command(name='m', aliases= ['metar', 'sa'], pass_context=True)
async def m(ctx, airport):
#metar
	# author = ctx.message.author
	await ctx.send(get_weather('metar', airport))

@client.command(name='fa', pass_context=True)
async def m(ctx, airport):
#gamet
	# author = ctx.message.author
	await ctx.send(get_weather('fa', airport))


@client.command(pass_context=True)
async def help(ctx):
#help
    emb = discord.Embed(title='Available commands list')
    emb.add_field(name='{}help'.format(PREFIX), value='List command', inline=False)
    emb.add_field(name=f'{PREFIX}t ({PREFIX}taf) XXXX', value='- Full forecast for airport', inline=False)
    emb.add_field(name=f'{PREFIX}m ({PREFIX}metar) XXXX', value='METAR for airport', inline=False)
    emb.add_field(name=f'{PREFIX}fa', value='Area weather forecast in GAMET format (RUSSIA only)', inline=False)
    emb.add_field(name='Also available in Telegram', value='https://telegram.me/usii_bot', inline=False)				  
    await ctx.send(embed=emb)

token = os.getenv('DISCORD_TOKEN')
client.run(token)
