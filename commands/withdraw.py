from classes import base_command
from globals import *
from helper import helper

from classes.user import *

import config, math, asyncio


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "withdraw"
        self.cmd = ["with"]
        self.args = True
        self.help = "[amount]"
        self.category = "Bank"
        self.description = "Withdraw money from your bank account"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 3)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if not user.has_bank():
            return await message.reply(
                embed=helper.embed(message, f":x: You **do not have a bank account** to withdraw your money!",
                                   ""))

        try:
            if str(clean[0]).lower() in data["others"]["everything"]:
                with_amount = user.get_bank_money()
            else:
                with_amount = int(clean[0])
                if with_amount < 1:
                    with_amount = 1
        except:
            return await message.reply(
                embed=helper.embed(message, f"",
                                   ":x: Please enter a valid number next time!"))

        if with_amount > user.get_bank_money():
            with_amount = user.get_bank_money()

        if user.get_bank_money() < with_amount:
            return await message.reply(
                embed=helper.embed(message, f"",
                                   ":x: You do not have enough money in your bank!"))

        user.add_money(with_amount)
        user.deduct_bank_money(with_amount)

        return await message.reply(
            embed=helper.embed(message, f"",
                               f"You have withdrawn :dollar: `${helper.money(with_amount)}` into your wallet!"))


commands.append(Command())
