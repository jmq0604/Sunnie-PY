import time

from classes import base_command
from globals import *
from helper import helper

from classes.server import *

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "support"
        self.cmd = []
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Sends the support server's invite link"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 600)

    async def run(self, client, message, clean, user):
        return await message.channel.send("https://discord.gg/eFF9pS3DRd")






commands.append(Command())
