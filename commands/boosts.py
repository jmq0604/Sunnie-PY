import time

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "boosts"
        self.cmd = ["boost", "booster"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Shows all the active boosters"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):

        body = ""
        boosts = user.get_booster_active()
        if len(boosts) < 1:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['chart']} Active Boosts", "You have **no active** boosters!"))

        for x in boosts:
            body += f"{data['items'][x]['emote']} **{data['items'][x]['name']}**: `{helper.time_human(user.get_booster_time(x) - time.time())}` Remaining \n"

        body += f"\n:dollar: **Total Boost:** `+${helper.money(user.get_revenue_extra())}/hr` `(+{helper.money(user.get_happiness_extra())}%)`"

        return await message.reply(
            embed=helper.embed(message, f"{data['emotes']['chart']} Active Boosts", body))




commands.append(Command())
