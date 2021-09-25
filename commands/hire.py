from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *

import random


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "hire"
        self.cmd = ["h"]
        self.args = False
        self.help = "<employee id>"
        self.category = "Employees"
        self.description = "Lists employees for hire or to hire them"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        if len(clean) > 0:
            id = str(clean[0]).lower()
            if id not in globals.employees:
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} That employee ID **does not exist** in the agency!".format(
                                                                  e=data["emotes"]["cross"])))

            if user.get_money() < user.get_emp_price(globals.employees[id]["price"]):
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} You do not have **enough cash** to afford the "
                                                              "contract!".format(e=data["emotes"]["cross"])))

            if user.get_revenue() < globals.employees[id]["cost_hour"]:
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} You do not have **enough revenue** to afford the "
                                                              "contract!".format(e=data["emotes"]["cross"])))

            user_emp = user.get_employee()
            if id in user_emp:
                return await message.reply(embed=helper.embed(message, "",
                                                                  "{e} You already have **hired** this employee before!".format(e=data["emotes"]["cross"])))

            user.deduct_revenue(globals.employees[id]["cost_hour"])
            user.deduct_money(user.get_emp_price(globals.employees[id]["price"]))
            user.add_emp(id, globals.employees[id])
            user.add_exp(random.randint(1, 30))

            return await message.reply(
                embed=helper.embed(message, "{e} Successfully Hired!".format(e=data["emotes"]["tick"]),
                                   "You have successfully hired **{n}**, you can do `{p}employees` to check everyone you have hired! You can also do `{p}fire id` to fire them in the future!".format(
                                       n=globals.employees[id]["name"],
                                       p=prefix)))
        else:
            embeds = {}
            for x in globals.employees:
                embeds[":running_shirt_with_sash: {n} | ID: {id}".format(n=globals.employees[x]["name"],
                                                                         id=x)] = "Cooking: `{c}`\nSocial: `{s}`\nTeamwork: `{t}`\n\nContract Price: `${p}`\nHourly Salary: `${h}/hr`\n‎‎‏‏‎ ‎‏‏‎ ‎".format(
                    h=globals.employees[x]["cost_hour"], p=helper.money(user.get_emp_price(globals.employees[x]["price"])),
                    c=globals.employees[x]["cooking"], s=globals.employees[x]["social"],
                    t=globals.employees[x]["teamwork"], m=globals.employees[x]["management"],
                    ma=globals.employees[x]["marketing"])

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\nUse `{p}hire [id]` to **hire** one of these employees!\nUse `{p}job` to **view** your shop's available jobs!\nUse `{p}employees [id]` to **view** your employee's stats!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "Sunnie Industry's Agency",
                                 "The agency updates it's hire list **hourly**, you will also have to pay them hourly, deducated by your revenue.".format(
                                     p=prefix),
                                 embeds=embeds)
            await message.reply(embed=embed)


commands.append(Command())
