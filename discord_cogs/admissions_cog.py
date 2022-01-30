from typing import Type, Dict, Callable
from discord.ext import commands

from data_model.admissions_data import AdmissionsData, SummaryData

class AdmissionsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admissions Officer has been loaded into {name} and is on the case!'.format(name = self.bot.user.name))
        print('=======================================')


    # Teach people how to use ratemychances command
    def __error_usage_message_ratemychances(self):
        usage = """
            Please use the command in the following format:
            
            !ratemychances program=PROGRAM_CODE average=AVERAGE [ type=TYPE ]

            where:
                - PROGRAM_CODE is the code from OUAC (only Waterloo program codes currently supported)
                - AVERAGE is your *percentage* based average (please convert before usings)
                - (optional) TYPE is one of [101, 105, 105D, 105F]
        """

        return usage

    def parse_args(self, args_list: list) -> dict:
        return dict(map(lambda x: x.split("="), args_list))

    # Double check the passed in arguments conform to what's expected
    # SIDE EFFECT:
    #   - This will properly cast as many arguments of arg_dict as possible
    #       (your strings will be gone.)
    async def check_required_args(self, ctx, arg_dict: Dict[str, str], required_args: Dict[str, Type], error_message_generatror: Callable) -> bool:
    
        for req_arg in required_args:
            if (req_arg not in arg_dict):
                await ctx.send('{req_field} was not specified.'.format(req_field = req_arg))
                await ctx.send(error_message_generatror())
                return False
            else:
                try:
                    arg_dict[req_arg] = required_args[req_arg](arg_dict[req_arg])
                except Exception as e:
                    await ctx.send('Could not cast {req_field} to be type {req_type}'.format(req_field = req_arg, req_type = required_args[req_arg].__name__))
                    await ctx.send(error_message_generatror())
                    return False
        return True

    @commands.command(name='ratemychances')
    async def on_message(self, ctx: commands.context.Context, *args):
        
        # Don't want to talk to ourself
        if (ctx.author.id == self.bot.user.id):
            return

        try:
            req_args = {'program': str, 'average': float}
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
