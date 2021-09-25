import time

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "ping"
        self.cmd = ["pong"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Pings the bot to see if its alive"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 15)

    async def run(self, client, message, clean, user):
        now = time.time() * 1000
        sent_message = await message.reply("Pinging...")
        later = time.time() * 1000

        return await sent_message.edit(content="", embed=helper.embed(message, f"{data['emotes']['red_alert']} Pong!", "**Latency:** `{latency}ms`\n**API Latency:** `{ping}ms`".format(ping=round(client.latency * 1000), latency=round(later-now))))



commands.append(Command())
