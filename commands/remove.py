import random, asyncio

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "remove"
        self.cmd = ["purge"]
        self.args = True
        self.help = "[mention]"
        self.category = "Admin"
        self.description = "Resets and deletes all of their progress"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 30)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        user_receive = helper.clean_message(clean[0])
        if not db.Exist("users", "id", user_receive):
            return await message.reply(
                embed=helper.embed(message, f"Profile Lookup",
                                   f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

        user_receive = UserData(user_receive)

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        try:
            await message.reply(embed=helper.embed(message, ":warning: COMPLETE RESET :warning:",
                                                   f"Please reply with a `yes` if you like to **restart and delete everything** in the database that belongs to them!"))
            msg = await client.wait_for('message', check=check, timeout=30)

            ans = helper.clean_message(msg.content).lower().strip()
            if ans == "yes" or ans == "y":

                user_receive.self_delete()

                return await message.reply(
                    embed=helper.embed(message, ":warning: COMPLETE RESET :warning:",
                                       f"**You have completely reseted all of your progress!**"))
            else:
                return await message.reply(
                    embed=helper.embed(message, ":warning: COMPLETE RESET :warning:",
                                       "Progress reset of progress has been canceled!"))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":warning: COMPLETE RESET :warning:",
                                   "You ran out of time! Please respond next time!".format(
                                       p=prefix)))

commands.append(Command())
