import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "create"
        self.cmd = ["found"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Create your own company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        if user.has_company():
            return await message.reply(
                embed=helper.embed(message, ":office: Company", f"You are already in an company!"))

        cost = data['company']['cost']
        if user.get_money() < cost:
            return await message.reply(
                embed=helper.embed(message, ":office: Company",
                                   "{e} You do not have enough money to purchase a company!".format(
                                       e=data["emotes"]["cross"])))

        tags = None
        if len(clean) > 1:
            tags = helper.clean_message(clean[1])

        if not tags or not len(tags) == 3:
            return await message.reply(
                embed=helper.embed(message, ":office: Company",
                                   f"You need to specify a **company tag** which is **3 letters** and **unique**.\n\nUsage: `{prefix}o create [tag]`"))

        if user.get_company(tags):
            return await message.reply(
                embed=helper.embed(message, ":office: Company", f"That tag has already been taken!"))

        user.deduct_money(cost)
        company = CompanyData(tags, message.author.id)
        company.add_role(message.author.id, "owner")
        company.reset_tax_time()

        return await message.reply(
            embed=helper.embed(message, ":office: Company", f"You just **created** your very own company! Good Luck!"))


commands.append(Command())
