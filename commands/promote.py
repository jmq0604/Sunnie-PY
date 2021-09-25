import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "promote"
        self.cmd = ["p"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Promotes someone to a higher rank in your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:
            if len(clean) > 1:
                user_invite = helper.clean_message(clean[1])
            else:
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: Please mention/tag the person you are promoting!"))

            if not db.Exist("users", "id", user_invite):
                return await message.reply(
                    embed=helper.embed(message, f"Profile Lookup",
                                       f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

            user_invite = UserData(user_invite)
            if str(user_invite.get_id()) == str(message.author.id):
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: You are unable to give yourself a promotion!"))

            if not user_invite.get_company() == user.get_company():
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f":x: You are unable to promote someone that is not in your company!"))

            user_role = user_invite.get_company_role()

            if role == 2:
                user.company.add_role(user_invite.get_id(), "recruiter")
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f"{data['emotes']['tick']} You have just promoted **{user_invite.get_name()}** to **Recruiter**!"))
            elif role == 1:
                if user_role > 3:
                    user.company.add_role(user_invite.get_id(), "recruiter")
                    return await message.reply(
                        embed=helper.embed(message, ":office: Company",
                                           f"{data['emotes']['tick']} You have just promoted **{user_invite.get_name()}** to **Recruiter**!"))
                elif user_role == 3:

                    if user.company.get_co_owner():
                        return await message.reply(
                            embed=helper.embed(message, ":office: Company",
                                               f"{data['emotes']['tick']} You can only have one **Co Owner** in a company!"))

                    user.company.add_role(user_invite.get_id(), "co_owner")
                    return await message.reply(
                        embed=helper.embed(message, ":office: Company",
                                           f"{data['emotes']['tick']} You have just promoted **{user_invite.get_name()}** to **Co Owner**!"))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
