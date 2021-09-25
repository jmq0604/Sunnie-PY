import time

from classes import base_command
from globals import *
from helper import helper

from classes.server import *

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "prefix"
        self.cmd = ["setprefix", "pp"]
        self.args = True
        self.help = "[prefix]"
        self.category = "Other"
        self.description = "Sets the prefix for the server"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 15)

    async def run(self, client, message, clean, user):

        split = message.content.split(' ')
        prefix = split[1].lower()

        if message.author.guild_permissions.administrator:
            if len(prefix) > 5 or len(prefix) < 1:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} Please make sure your new prefix is below 5 characters".format(
                                           e=data["emotes"]["cross"])))

            server = ServerData(message.guild.id)
            server.set_prefix(prefix)

            return await message.reply(
                embed=helper.embed(message, "", f"Prefix has been set to `{prefix}`"))
        else:
            return await message.reply(
                embed=helper.embed(message, "Permission Error", f"Only `administrators` have access to this command!"))






commands.append(Command())
