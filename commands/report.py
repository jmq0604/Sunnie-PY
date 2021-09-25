import time

from classes import base_command
from globals import *

from helper import helper
import config

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "report"
        self.cmd = ["bug", "reportbug", "suggest"]
        self.args = True
        self.help = "[message]"
        self.category = "Other"
        self.description = "Report any bugs or errors that you have faced using the bot"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 6000)

    async def run(self, client, message, clean, user):

        channel = client.get_channel(int(config.report_channel))
        await channel.send(f"```Report By: {message.author.display_name}\nMessage: {message.content}```")

        return await message.reply(
            embed=helper.embed(message, "Report Sent", "Thank you for sending your report! We will get back to you as soon as possible!"))


commands.append(Command())
