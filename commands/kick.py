import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "kick"
        self.cmd = ["ban"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Kicks one of your members from your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:
            if len(clean) > 1:
                user_invite = helper.clean_message(clean[1])
            else:
                return await message.reply(
                    embed=helper.embed(message, ":office: Company", f"Please mention/tag the person you are kicking!"))

            if not db.Exist("users", "id", user_invite):
                return await message.reply(
                    embed=helper.embed(message, f"Profile Lookup",
                                       f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

            user_invite = UserData(user_invite)
            if str(user_invite.get_id()) == str(message.author.id):
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: You are unable to kick yourself!"))

            if not user_invite.get_company() == user.get_company():
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: You are unable to kick someone that is not in your company!"))

            user.company.remove_role(user_invite.get_id())
            return await message.reply(
                embed=helper.embed(message, ":office: Company",
                                   f"You have successfully kicked **{user_invite.get_name()}** from your company!"))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
