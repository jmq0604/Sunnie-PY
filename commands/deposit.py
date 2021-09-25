from classes import base_command
from globals import *
from helper import helper

from classes.user import *

import config, math, asyncio


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "deposit"
        self.cmd = ["dep"]
        self.args = True
        self.help = "[amount]"
        self.category = "Bank"
        self.description = "Deposits money into your bank account"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 3)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if not user.has_bank():
            return await message.reply(
                embed=helper.embed(message, f":x: You **do not have a bank account** to deposit your money!",
                                   ""))

        try:
            if str(clean[0]).lower() in data["others"]["everything"]:
                dep_amount = user.get_max_deposit() - user.get_bank_money()
            else:
                dep_amount = int(clean[0])
                if dep_amount < 1:
                    dep_amount = 1
        except:
            return await message.reply(
                embed=helper.embed(message, f"",
                                   ":x: Please enter a valid number next time!"))

        if dep_amount > user.get_money():
            dep_amount = user.get_money()

        if user.get_bank_money() + dep_amount > user.get_max_deposit():
            dep_amount = user.get_max_deposit() - user.get_bank_money()

        user.deduct_money(dep_amount)
        user.add_bank_money(dep_amount)

        return await message.reply(
            embed=helper.embed(message, f"",
                               f"You have deposited :dollar: `${helper.money(dep_amount)}` into your bank!"))


commands.append(Command())
