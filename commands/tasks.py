from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *

import random


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "tasks"
        self.cmd = ["task", "g"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Lists all the daily task you have"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        embeds = {}
        for x in globals.daily_tasks:
            embeds[":running_shirt_with_sash: {n} | ID: {id}".format(n=globals.employees[x]["name"],
                                                                     id=x)] = "Cooking: `{c}`\nSocial: `{s}`\nTeamwork: `{t}`\n\nContract Price: `${p}`\nHourly Salary: `${h}/hr`\n‎‎‏‏‎ ‎‏‏‎ ‎".format(
                h=globals.employees[x]["cost_hour"], p=helper.money(user.get_emp_price(globals.employees[x]["price"])),
                c=globals.employees[x]["cooking"], s=globals.employees[x]["social"],
                t=globals.employees[x]["teamwork"], m=globals.employees[x]["management"],
                ma=globals.employees[x]["marketing"])

        embed = helper.embed(message, "Daily Tasks",
                             "".format(p=prefix),
                             embeds=embeds)
        await message.reply(embed=embed)


commands.append(Command())
