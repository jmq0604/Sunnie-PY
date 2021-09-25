import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "corp"
        self.cmd = ["name", "n"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Rename your company's name"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:
            try:
                name = helper.clean_message(" ".join(clean[1:]))
                if len(name) > 15 or len(name) < 5:
                    return await message.reply(
                        embed=helper.embed(message, ":office: Company",
                                           f":x: Please make sure your company's name is between **5 - 15 characters long**!"))

                user.company.set_name(name)
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f"{data['emotes']['tick']} You have officially set your company's name to **{name}**!"))
            except:
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: Please use a valid name for your company!"))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
