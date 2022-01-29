
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


    # Teach people how to use ratemychances command
    def __usage_message_ratemychances(self):
        usage = """
            Please use the command in the following format:
            
            !ratemychances program=PROGRAM average=AVERAGE [ type=TYPE ]

            where:
                - (optional) TYPE is one of [101, 105, 105D, 105F]
        """

        return usage


    @commands.command(name='ratemychances')
    async def on_message(self, ctx: commands.context.Context, *args):
        
        # Don't want to talk to ourself
        if (ctx.author.id == self.bot.user.id):
            return

        if (len(args) == 0):
            await ctx.send(self.__usage_message_ratemychances())
            return

        print(args)
        
        await ctx.send('no')
