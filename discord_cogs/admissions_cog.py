from msilib import change_sequence
from discord.ext import commands

from data_model.admission_types import GradeAverage, Program
from data_model.admissions_data import AdmissionsData
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

        arg_program = arg_dict['program']
        arg_average = arg_dict['average']

        admissions_data = AdmissionsData(2021)

        summary_data = admissions_data.get_program_data(Program.get_code_to_long(arg_program))

        chances_message = "(Based on the data from last year's sheet)\n"

        if (summary_data.num_applicants == 0):
            chances_message += "Err.. we don't have any data for {program_long}..".format(program_long = Program.get_code_to_long(arg_program))
            chances_message += "But it looks like UW is planning to have an intake of {enrollment} this year - so someone has to get in.. probably?".format(
                enrollment = Program.get_enrollment_numbers(arg_program)
            )
            await ctx.send(chances_message)
            return

        chances_message += "For the program of {program_long}, we have a data sample of {applicants}, and the reported averages ranged from {low_avg:.2f} to {high_avg:.2f}\n".format(
            program_long = Program.get_code_to_long(arg_program),
            applicants = summary_data.num_applicants,
            low_avg = summary_data.low,
            high_avg = summary_data.high
        )

        if (arg_average < summary_data.low):
            chances_message += "So yea.. best of luck!\n"
        elif (arg_average <= summary_data.high):
            chances_message += "So it looks like you have shot?\n"
        else:
            chances_message += "Looks like you're pretty competitive o.o\n"


        chances_message += "(Keep in mind we're only seeing {pool_size_pct:.2f} \% of the pool)".format(
            pool_size_pct = summary_data.num_applicants / Program.get_enrollment_numbers(arg_program) * 100
        )

        await ctx.send(chances_message)
