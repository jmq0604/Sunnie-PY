import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "delete"
        self.cmd = ["remove"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Dissolves your company, removing everything about it"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 1:
            def check(m):
                if m.author.id == message.author.id:
                    return True
                return False

            try:

                await message.reply(embed=helper.embed(message, ":warning: Company Deletion In-Progress",
                                                       "Please reply with a `yes` if like to delete your company!"))
                msg = await client.wait_for('message', check=check, timeout=30)

                ans = helper.clean_message(msg.content).lower()
                if ans == "yes" or ans == "y":

                    user.company.self_delete()

                    return await message.reply(
                        embed=helper.embed(message, "Company Deleted",
                                           f"You have successfully dissolve your company!"))
                else:
                    return await message.reply(
                        embed=helper.embed(message, ":x: Company Deletion Failed",
                                           "The company will not be deleted!"))
            except asyncio.TimeoutError:
                return await message.reply(
                    embed=helper.embed(message, ":x: Company Deletion Failed",
                                       "You ran out of time! Please respond next time!".format(
                                           p=prefix)))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
