from classes import base_command
from globals import *
from helper import helper

from classes.user import *

import config, math, asyncio


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "claim"
        self.cmd = ["cl", "int"]
        self.args = False
        self.help = ""
        self.category = "Bank"
        self.description = "Claims interest earnt from your bank account"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 3)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if not user.has_bank():
            return await message.reply(
                embed=helper.embed(message, f":x: You **do not have a bank account** to claim interest from!",
                                   ""))

        if user.get_claim() == 0:
            return await message.reply(
                embed=helper.embed(message, f":x: Your interest claim is empty!",
                                   ""))

        claim = user.get_claim()

        user.add_money(claim)
        user.deduct_claim(claim)

        return await message.reply(
            embed=helper.embed(message, f"",
                               f"You just claimed :dollar: `${helper.money(claim)}` from your bank!"))


commands.append(Command())
