from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "tutorial"
        self.cmd = ["howto", 'tut']
        self.args = False
        self.help = ""
        self.cooldown = 600
        self.category = "Other"
        self.description = "DMs you the game's guide"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user):
            try:
                await message.author.send(embed=helper.embed(message, "<:welcome2:856195655583924265> Welcome to Sunnie Restaurant <:welcome:856195642148782081>", config.help_embed))
            except:
                return await message.reply(embed=helper.embed(message, "Ultimate Guide!", "You have DM set on disabled! I am not able to DM you the guide!"))


            return await message.reply(embed=helper.embed(message, "Ultimate Guide!", "I have sent you a **DM** on how to play the game!"))


commands.append(Command())
