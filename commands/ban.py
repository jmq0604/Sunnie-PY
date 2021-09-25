import random, asyncio

from classes.user import UserData
from classes.server import ServerData

from classes import base_command
from globals import *
from helper import helper

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "ban"
        self.cmd = ["blacklist"]
        self.args = True
        self.help = "[add/remove] [user/server] [userid/serverid]"
        self.category = "Admin"
        self.description = "Adds the user/server into the ban zone"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 30)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if len(clean) < 3:
            return await message.reply(
                embed=helper.embed(message, ":warning: BAN/BLACKLISTING :warning:",
                                   f"Please use the right format, `{self.help.format(p=prefix)}` next time!"))

        ban_id =  helper.clean_message(clean[2])

        if clean[1].lower() == "server":
            ban_id = ServerData(ban_id)
            if clean[0].lower() == "add":
                ban_id.add_ban()
            else:
                ban_id.remove_ban()
        else:
            ban_id = UserData(ban_id)
            if clean[0].lower() == "add":
                ban_id.add_ban()
            else:
                ban_id.remove_ban()

        return await message.reply(
            embed=helper.embed(message, ":warning: BAN/BLACKLISTING :warning:",
                               "You have added the user/server into the ban list!".format(
                                   p=prefix)))

commands.append(Command())
