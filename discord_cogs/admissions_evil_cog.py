from discord.ext import commands
import random
from typing import Dict

from data_model.admission_types import Program
from data_model.admissions_data import AdmissionsData
from types_util import ApplicantField

class AdmissionsEvilCog(commands.Cog):
    # This class focuses on commands related to admissions - tends to meme it up a little, be a little scarcastic

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admissions Evil Officer has been loaded into {name} and is on the case!'.format(name = self.bot.user.name))
        print('=======================================')


    def reject_command(self, ctx: commands.context.Context) -> str:
        rejections = [
            "Bro you're grade 11 stop asking... go play outside or something.. smh",
            "{asker} is a massive troll who should be banned from here and the applicants server".format(asker = ctx.author.name),
            "no",
            "I'm tired, ask again later",
            "why do you think I could accurately tell you this lol?"
        ]

        return random.choice(rejections) + "\n"

    def high_average(self, ctx: commands.context.Context, program_long: str) -> str:
        messages = [
            "WTF {asker}, you're cracked".format(asker = ctx.author.name),
            "{asker}.. {program_long} is a backup for you isn't?".format(asker = ctx.author.name, program_long=program_long),
            "O.o could I just pay you to write my tests?"
        ]
        return random.choice(messages) + "\n"

    def mid_average(self, ctx: commands.context.Context, program_long: str) -> str:
        messages = [
            "I mean.. looks like others applied with around your average last year.. maybe you could start a friend group (and get off discord)",
            "You make the RNG cutoff. Congrats. Please stand by, human admissions officers are rolling the dice for you as we speak",
            "It's possible.. but so is me becoming sentient.. just saying"
        ]
        return random.choice(messages) + "\n"

    def low_average(self, ctx: commands.context.Context, program_long: str) -> str:
        messages = [
            "... yea...{asker}... so I have bad news...".format(asker = ctx.author.name),
            "On the bright side {program_long} probably defers into ... something else.. (idk you better pray)".format(program_long = program_long),
            "{asker}.. I hope you know you're not in the University of {w_city} discord server".format(
                asker = ctx.author.name,
                w_city = random.choice(['Walvis Bay', 'Willich', 'Winterhude', 'Whangarei', 'Weymouth', 'Wedi'])
            ),
            "gg no re",
            "it's time to start finding people to bribe"
        ]
        return random.choice(messages) + "\n"

    async def rate_my_chances(self, ctx: commands.context.Context, arg_dict: Dict[str, ApplicantField]):
        # Don't want to talk to ourself
        if (ctx.author.id == self.bot.user.id):
            return

        arg_program = arg_dict['program']
        arg_average = arg_dict['average']

        admissions_data = AdmissionsData(2021)

        summary_data = admissions_data.get_program_data(Program.get_code_to_long(arg_program))

        action_die = random.randrange(0, 100)

        if (action_die <= 20):
            await ctx.send(self.reject_command(ctx))
            return

        chances_message = "(Based on the data from last year's sheet)\n"

        if (action_die <= 40):
            await ctx.send("Legit what would you even use {program_long} for..?".format(program_long = Program.get_code_to_long(arg_program)))


        if (summary_data.num_applicants == 0):
            chances_message += "Damn no one even applied to {program_long}..".format(program_long = Program.get_code_to_long(arg_program))
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
            chances_message += self.low_average(ctx, Program.get_code_to_long(arg_program))
        elif (arg_average <= summary_data.high):
            chances_message += self.mid_average(ctx, Program.get_code_to_long(arg_program))
        else:
            chances_message += self.high_average(ctx, Program.get_code_to_long(arg_program))


        chances_message += "(Keep in mind we're only seeing ({numerator} / {denominator}) =  {pool_size_pct:.2f} \% of the pool)".format(
            numerator = summary_data.num_applicants,
            denominator = Program.get_enrollment_numbers(arg_program),
            pool_size_pct = summary_data.num_applicants / Program.get_enrollment_numbers(arg_program) * 100
        )

        await ctx.send(chances_message)
