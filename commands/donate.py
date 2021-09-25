import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "donate"
        self.cmd = ["give"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Donates money to your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        try:
            if str(clean[1]).lower() in data["others"]["everything"]:
                donation = user.get_money()
            else:
                donation = int(helper.clean_message(clean[1]).strip())
                if donation < 500:
                    donation = 500

            if donation > user.get_money():
                return await message.reply(
                    embed=helper.embed(message, f"",
                                       ":x: You can't donate more than what you have!"))

            user.company.add_money(donation)
            user.deduct_money(donation)

            return await message.reply(
                embed=helper.embed(message, f"Donation Successful",
                                   f"You have just donated :dollar: `${helper.money(donation)}` to **{user.company.get_name()}**!"))

        except:
            return await message.reply(
                embed=helper.embed(message, f"",
                                   ":x: Please enter a valid number next time!"))


commands.append(Command())
