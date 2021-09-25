import random, asyncio, time, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "company"
        self.cmd = ["co", "o", "clan"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "Sows everything you can do in a company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        args = ""
        if len(clean) > 0:
            args = str(clean[0]).lower()

        if args:
            for cmd in commands:
                if args in cmd.cmd and cmd.child and cmd.category == "Company":

                    if not cmd.name == "create":
                        if not user.has_company():
                            return await message.reply(
                                embed=helper.embed(message, ":office: Company",
                                                   f"You are **not in an company**, please either **create** one or **join** one!"))

                    return await cmd.prerun(client, message, clean, UserData(message.author.id, message.channel.id))

        else:
            if not user.has_company():
                return await message.reply(
                    embed=helper.embed(message, ":office: Company",
                                       f"You are **not in an company**, please either **create** one or **join** one!"))

            modules_str = "‎‎‏‏‎ ‎‏‏‎ "
            for x in user.company.get_modules():
                modules_str += f"{data['company']['module'][x]['emote']} {data['company']['module'][x]['name']} ━  `${helper.money(user.company.get_modules_income(x))}/hr` | `{helper.money(user.company.get_modules_capacity(x))} cap`\n ‎‏‏‎ "

            company = user.company
            embed = helper.embed(message, "{e} {name}".format(e=data["emotes"]["company"], name=company.get_name()),
                                 "*{slogan}*".format(slogan=company.get_motto()),
                                 embeds={
                                     "Owner": "{e} {owner}".format(e=data["emotes"]["owner"], owner=f"<@{user.company.get_owner()}>"),
                                     "Members": "{e} {total_members}/{max}".format(max=user.company.get_max_cap(),e=data["emotes"]["user"], total_members=helper.money(user.company.total_members())),
                                     "Cash": "{e} ${c}".format(e=data["emotes"]["cash"], c=helper.money(user.company.get_money())),
                                     "Revenue ( hourly )": "{e} ${c} | {ea} {cm}".format( e=data["emotes"]["revenue"],ea=data["emotes"]["pizza"],
                                                                                              c=helper.money(
                                                                                                  user.company.get_income()),
                                                                                              cm=helper.money(
                                                                                                  user.company.get_income_sold())),
                                     "Total Sold": "{e} {c}".format(e=data["emotes"]["pizza"], c=helper.money(user.get_total_sold())),
                                     "Capacity": "{e} {h}".format(e=data["emotes"]["capacity"], h=helper.money(user.company.get_capacity())),
                                     "Tax Return": "{e} {t} left".format(e=data["emotes"]["tax"], t=helper.time_remaining(int(time.time() - user.company.get_tax_time()), config.company_cooldown)),
                                     "Modules": modules_str,
                                     "Level": "{e} {c} | {exp}/{max}".format(max=helper.money(user.company.get_required_exp()),
                                                                             exp=helper.money(user.company.get_exp()),
                                                                             e=data["emotes"]["level"],
                                                                             c=helper.money(user.company.get_level()))
                                 })

            await message.reply(embed=embed)



commands.append(Command())
