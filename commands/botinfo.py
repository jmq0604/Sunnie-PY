import time, psutil, discord, os, asyncio

from classes import base_command
from globals import *
from helper import helper

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "botinfo"
        self.cmd = ["botstat"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Returns the bot's statistics and information"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 60)

    async def run(self, client, message, clean, user):

        sent_message = await message.reply("Loading...")

        embeds = {}
        embeds[f'{data["emotes"]["memory"]} Memory'] = f'`{psutil.virtual_memory()[2]}%`'
        embeds[f'{data["emotes"]["cpu"]} CPU'] = f'`{psutil.cpu_percent(1)}%`'
        embeds[f'{data["emotes"]["disk"]} Disk'] = f'`{psutil.disk_usage(os.getcwd())[3]}%`'

        total_channel = 0
        for guild in client.guilds:
            total_channel += len(guild.channels)
            await asyncio.sleep(0)

        embeds[f'{data["emotes"]["user"]} Users'] = f'`{helper.money(len(client.users))}`'
        embeds[f'{data["emotes"]["server"]} Servers'] = f'`{helper.money(len(client.guilds))}`'
        embeds[f'{data["emotes"]["tv"]} Channels'] = f'`{helper.money(total_channel)}`'

        return await sent_message.edit(content="",embed=helper.embed(message, f"Bot Info", f"", embeds=embeds, inline=True))



commands.append(Command())
