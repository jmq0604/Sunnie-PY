import time

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "clean"
        self.cmd = ["wash", "c"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Cleans your pizzeria to keep customers happy"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):

        if time.time() - user.get_clean() > 86400:
            user.reset_clean()
            return await message.reply(embed=helper.embed(message, "", "{e} You have **cleaned** your shop!".format(e=data["emotes"]["tick"])))
        else:
            return await message.reply(
                embed=helper.embed(message, "", "{e}  You can clean again in **{t}**!".format(e=data["emotes"]["cross"], t=helper.time_remaining(int(time.time() - user.get_clean()), 86400))))



commands.append(Command())
