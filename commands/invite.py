from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "invite"
        self.cmd = ["invites"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Sends the bot's invite link"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 60)

    async def run(self, client, message, clean, user):

        embeds = helper.embed(message, "Invite Link", "Click [here](https://discord.com/api/oauth2/authorize?client_id=417174198843211776&permissions=8&scope=bot) to **invite the bot** into your own server!".format(e=data["emotes"]["tick"]))
        embeds.url = 'https://discord.com/api/oauth2/authorize?client_id=417174198843211776&permissions=8&scope=bot'
        return await message.channel.send(embed=embeds)



commands.append(Command())
