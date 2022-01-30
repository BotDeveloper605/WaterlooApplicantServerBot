from discord.ext import commands

from data_model.admission_types import GradeAverage, Program
from discord_cogs.argument_handler import ArugmentHandler

class AdmissionsCog(commands.Cog):
    # This class focuses on commands related to admissions

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admissions Officer has been loaded into {name} and is on the case!'.format(name = self.bot.user.name))
        print('=======================================')


    @commands.command(name='ratemychances')
    async def on_message(self, ctx: commands.context.Context, *given_args):
        # Don't want to talk to ourself
        if (ctx.author.id == self.bot.user.id):
            return

        req_args = {'program': Program, 'average': GradeAverage}
        opt_args = {}

        arg_dict = await ArugmentHandler.parse_command(ctx, given_args, req_args, opt_args)

        if arg_dict is None:
            return
        
        await ctx.send('no')
