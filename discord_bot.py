
# =================== Fix asyncio ======================
import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()
# ======================================================

import os
import discord
from dotenv import load_dotenv

from data_model.admissions_data import AdmissionsData, SummaryData

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)