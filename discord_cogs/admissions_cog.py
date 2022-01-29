
# ========================= Fix asyncio ============================
# (need this if running in interactive python terminal on VS Code)
# import nest_asyncio
# nest_asyncio.apply()
# __import__('IPython').embed()
# ==================================================================

from discord.ext import commands
import discord

from data_model.admissions_data import AdmissionsData, SummaryData

class AdmissionsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admissions Officer Cog has been loaded into {name} and is on the case!'.format(name = self.bot.user.name))
        print('=======================================')

    @commands.command(name='ratemychancesbot')
    async def on_message(self, ctx: commands.context.Context, arg):
        print(arg)

        await ctx.send('no')
