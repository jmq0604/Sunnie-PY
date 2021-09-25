import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "invite"
        self.cmd = ["seek"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Invites a member to your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 3:

            if user.company.total_members() >= user.company.get_max_cap():
                return await message.reply(
                    embed=helper.embed(message, ":office: Company", f"You have reached the maximum people you can hire into your company!"))

            if len(clean) > 1:
                user_invite = helper.clean_message(clean[1])
            else:
                return await message.reply(
                    embed=helper.embed(message, ":office: Company", f"Please mention/tag the person you are inviting!"))

            if not db.Exist("users", "id", user_invite):
                return await message.reply(
                    embed=helper.embed(message, f"Profile Lookup",
                                       f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

            user_invite = UserData(user_invite)

            if user_invite.has_company():
                return await message.reply(
                    embed=helper.embed(message, ":office: Company", f"You are unable to invite someone who is already in a company!"))

            def check(m):
                if str(m.author.id) == user_invite.get_id() and m.channel.id == message.channel.id and m.content == "accept":
                    return True

                return False

            try:
                await message.channel.send(embed=helper.embed(message, "Company Invitation", f"<@{user_invite.get_id()}>, You have been invited to **{user.company.get_name()}**, please type in `accept` to join the company!"))
                msg = await client.wait_for('message', check=check, timeout=30)

                user.company.add_role(user_invite.get_id(), "member")
                await message.channel.send(embed=helper.embed(message, "Company Invitation", f"<@{user_invite.get_id()}>, You have just joined **{user.company.get_name()}**!"))

            except asyncio.TimeoutError:
                return await message.reply(
                    embed=helper.embed(message, ":x: Company Invitation In-Completed",
                                       "As they did not reply to the invitation, it will now be cancelled!"))
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
