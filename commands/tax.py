import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "tax"
        self.cmd = ["taxes", "taxreturn"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Does your weekly tax returns for your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:
            user.company.reset_tax_time()
            return await message.reply(
                embed=helper.embed(message, ":office: Company - Tax Returned",
                                   f"**You just filed your tax returns!**"))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
