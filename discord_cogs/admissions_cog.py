from typing import Dict, Callable
from discord.ext import commands
from numpy import average

from data_model.admissions_data import AdmissionsData
from data_model.admission_types import ApplicantField, GradeAverage, Program

class AdmissionsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admissions Officer has been loaded into {name} and is on the case!'.format(name = self.bot.user.name))
        print('=======================================')

    # Teach people how to use ratemychances command - todo add more options? (or new commands)
    def __error_usage_message_ratemychances(self):
        return """
            Please use the command in the following format:
            
            !ratemychances program=PROGRAM_CODE average=AVERAGE

            where:
                - {program}
                - {average}
        """.format(
            program = Program.invalid_hint(), 
            average = GradeAverage.invalid_hint())


    def parse_args(self, args_list: list) -> dict:
        return dict(map(lambda x: x.split("="), args_list))

    # Double check the passed in arguments conform to what's expected
    # SIDE EFFECT:
    #   - This will properly cast as many arguments of arg_dict as possible
    #       (your strings will be gone.)
    async def check_required_args(self, ctx, arg_dict: Dict[str, str], required_args: Dict[str, ApplicantField], error_message_generatror: Callable) -> bool:
        for req_arg in required_args:
            if (req_arg not in arg_dict):
                # We could not find the require field
                await ctx.send('{req_field} was not specified.'.format(req_field = req_arg))
                await ctx.send(error_message_generatror())
                return False
            elif (not required_args[req_arg].is_valid(arg_dict[req_arg])):
                # We found the field, but it is not the right type
                await ctx.send(required_args[req_arg].invalid_hint())
                await ctx.send(error_message_generatror())
                return False
            else:
                # We found the type and it's what we expect
                arg_dict[req_arg] = required_args[req_arg].translate(arg_dict[req_arg])
        return True

    @commands.command(name='ratemychances')
    async def on_message(self, ctx: commands.context.Context, *args):
        # Don't want to talk to ourself
        if (ctx.author.id == self.bot.user.id):
            return

        try:
            req_args = {'program': Program, 'average': GradeAverage}
            arg_dict = self.parse_args(args)

            # A radioactively toxic line of code, but damn, it felt good to write 
            if (not await self.check_required_args(ctx, arg_dict, req_args, self.__error_usage_message_ratemychances)):
                # We ran into an issue that we already caught.. don't worry about it any more.
                return
            
            # ======= After this line, we should be guaranteed required arguments & matching types =====



        except Exception as e:
            await ctx.send('Error processing request')

            if (len(e.args) > 0):
                await ctx.send("Specificaly... {error}".format(error = e.args[0]))

            await ctx.send(self.__error_usage_message_ratemychances())
            return

        await ctx.send('no')
