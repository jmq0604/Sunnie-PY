import time

from classes import base_command
from globals import *
from helper import helper

from classes.server import *

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "rawguide"
        self.cmd = ["textguide"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Sends the guide into the channel instead of DM"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 200)

    async def run(self, client, message, clean, user):

        if message.author.guild_permissions.administrator:
            await message.channel.send(embed=helper.embed(message,
                                                         "<:welcome2:856195655583924265> Welcome to Sunnie Restaurant <:welcome:856195642148782081>",
                                                         config.help_embed))
            return await message.channel.send("https://discord.gg/eFF9pS3DRd")
        else:
            return await message.reply(
                embed=helper.embed(message, "Permission Error", f"Only `administrators` have access to this command!"))






commands.append(Command())
