import os
from dotenv import load_dotenv
from discord.ext import commands

from discord_cogs.admissions_cog import AdmissionsCog
from discord_cogs.admissions_evil_cog import AdmissionsEvilCog

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix = '!')

    bot.add_cog(AdmissionsCog(bot))    
    bot.add_cog(AdmissionsEvilCog(bot))

    bot.run(TOKEN)