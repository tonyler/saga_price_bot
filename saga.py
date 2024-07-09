import discord
from discord.ext import commands, tasks
import requests
import os

intents = discord.Intents.all()
intents.typing = True
intents.presences = True
intents.message_content = True  

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Watching Osmosis"))
    print(f'You have logged in as {bot.user}')
    update.start()


async def change_presence(price,change24): 
    nickname = f'{price}$'
    for guild in bot.guilds:
        await guild.me.edit(nick=nickname)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=change24))

osmosis_api = "https://api-osmosis.imperator.co/tokens/v2/saga"
gecko_api = "https://api.coingecko.com/api/v3/simple/price?ids=saga-2&vs_currencies=usd"
async def get_price(): 
    try:
        data = requests.get(osmosis_api)
        response =  data.json()
        price = round(float(response[0]["price"]),2)
        change24 = round (float(response[0]["price_24h_change"]),2)
        change24 = f"24h: {change24}%"
    except: 
         data = requests.get(gecko_api)
         response = data.json()
         price = round(float(response["saga-2"]["usd"]),2)
         change24 = "Coingecko"
    return price, change24
     
    
@tasks.loop(minutes = 2)
async def update():
        price, change24 = await get_price()
        print ("Updated data ✅")
        await change_presence(price, change24)
        print ("Updated Status ✅")



BOT_TOKEN = os.environ.get("DISCORD_KEY")
bot.run(BOT_TOKEN)