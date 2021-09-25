import asyncio
import random, time, config

from classes import base_command
from classes.user import UserData

from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "cooldown"
        self.cmd = ["co"]
        self.args = False
        self.help = ""
        self.cooldown = 2
        self.category = "Basic"
        self.description = "Shows you all the cooldown you have for your commands"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        embeds = {}

        def cooldown(difference=None, cooldown=None, dict=None):
            if dict:
                if not dict in user_cooldown:
                    return f":white_check_mark: READY"
                else:
                    difference = user_cooldown[dict]['time']

            if round(int(cooldown) - int(int(time.time() - difference))) < 0:
                return f":white_check_mark: READY"
            else:
                return f":x: {helper.time_remaining(int(time.time() - difference), cooldown)}"

        embeds["Daily"] = "{e}".format(e=cooldown(user.get_daily_time(), config.clean_time))
        embeds["Clean"] = "{e}".format(e=cooldown(user.get_clean(), config.clean_time))
        embeds["Work"] = "{e}".format(e=cooldown(dict=str(f"{message.author.id}_work"), cooldown=commands_dict["work"].cooldown))
        embeds["Tips"] = "{e}".format(e=cooldown(dict=str(f"{message.author.id}_tips"), cooldown=commands_dict["tips"].cooldown))

        if user.has_company():
            embeds["Overtime"] = "{e}".format(e=cooldown(dict=str(f"{message.author.id}_overtime"), cooldown=commands_dict["overtime"].cooldown))

        for x in list(data["skills"].keys()):
            if user.get_level() >= data["skills"][x]["level"]:
                embeds[f"{data['skills'][x]['name']}"] = "{e}".format(e=cooldown(dict=str(f"{message.author.id}_{x}"), cooldown=commands_dict[x].cooldown))

        return await message.reply(
            embed=helper.embed(message, ":hourglass_flowing_sand: Cooldown",
                               f"", embeds=embeds))

commands.append(Command())
