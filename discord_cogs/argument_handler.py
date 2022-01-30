from dis import Instruction
from typing import Dict, Any
from discord.ext import commands
from functools import reduce

from data_model.admission_types import ApplicantField


class ArugmentHandler():
    # This class does the heavy lifting on parsing arguements, casting them and related handling errors 

    @classmethod
    # Teach people how to use ratemychances command - todo add more options? (or new commands)
    # Make this error a generic template - or create an error message command?
    def error_usage_message(cls, command_name: str, req_args: Dict[str, ApplicantField] = {}, opt_args: Dict[str, ApplicantField] = {}) -> str:
        usage = "\n\n*****Please use the command in the following format*****:\n"
        usage += "!" + command_name 
        usage += reduce(lambda x, y : x + " {arg_name}={val_name} ".format(arg_name = y[0], val_name = y[1].field_name()), req_args.items(), "")
        usage += reduce(lambda x, y : x + " [ {arg_name}={val_name} ] ".format(arg_name = y[0], val_name = y[1].field_name()), opt_args.items(), "")
        usage += "\n\n\t\tWhere:\n\n"
        usage += reduce(lambda x, y : x + "\t\t - {instructions}\n".format(instructions = y[1].invalid_hint()), req_args.items(), "")
        usage += reduce(lambda x, y : x + "\t\t - (OPTIONAL) {instructions}\n".format(instructions = y[1].invalid_hint()), opt_args.items(), "")
        return usage

    @classmethod
    # Try to cast the provided arguments into the formats that we would expect
    # given_args: what's passed to us through discord
    # command_args: the design pattern to what's pre-expected
    # SIDE EFFECT: 
    #   - This will mutate the provided given_args dictionary to turn, casting as we check
    def cast_args(cls, given_args: Dict[str, str], command_args: Dict[str, ApplicantField], optional: bool = False) -> str:
        for arg in command_args:

            if (optional and arg not in given_args):
                # Free pass if we didn't need this one anyways
                continue

            if (arg not in given_args):
                return "{required_argument} was not specified.".format(required_argument = arg)
            elif (not command_args[arg].is_valid(given_args[arg])):
                return command_args[arg].invalid_hint()
            else:
                given_args[arg] = command_args[arg].translate(given_args[arg])

        return ""

    @classmethod
    # Parse command arguments that were given - caller responsibility for errors
    def parse_args(cls, args_list: list) -> Dict[str, str]:
        return dict(map(lambda x: x.split("="), args_list))

    @classmethod
    # Double check the passed in arguments conform to what's expected
    # TODO: scope creep? split into two - one for arg checking.. the other for 
    async def check_args(cls, ctx: commands.context.Context, arg_dict: Dict[str, str], required_args: Dict[str, ApplicantField] = {}, optional_args: Dict[str, ApplicantField] = {}) -> bool:

        required_result = cls.cast_args(arg_dict, required_args)
        optional_result = cls.cast_args(arg_dict, optional_args, True)

        if (len(required_result) > 0 or len(optional_result) > 0):
            await ctx.send(required_result if len(required_result) > 0 else optional_result)
            await ctx.send(cls.error_usage_message(ctx.command, required_args, optional_args))
            return False
        return True

    @classmethod
    # Try to parse given arguments and return an accurately parsed dictionary of expected types
    async def parse_command(cls, ctx: commands.context.Context, given_args: list, required_args: Dict[str, ApplicantField] = {}, optional_args: Dict[str, ApplicantField] = {}) -> Dict[str, Any]:
        try:
            arg_dict = cls.parse_args(given_args)

            # A radioactively toxic line of code, but damn, it felt good to write 
            if (not await ArugmentHandler.check_args(ctx, arg_dict, required_args, optional_args)):
                return None

        except Exception as e:
            await ctx.send(cls.error_usage_message(ctx.command.name, required_args, optional_args))
            return None

        return arg_dict

