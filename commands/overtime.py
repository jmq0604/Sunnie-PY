import asyncio
import random

from classes import base_command
from classes.user import UserData

from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "overtime"
        self.cmd = ["ot"]
        self.args = False
        self.help = ""
        self.cooldown = 1800
        self.category = "Company"
        self.description = "Play a company game to earn some money by working in your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if not user.has_company():
            return await message.reply(
                embed=helper.embed(message, ":office: Company",
                                   f"You are **not in an company**, please either **create** one or **join** one!"))

        pizzas = list(data['pizza']['types'].keys())

        random.shuffle(pizzas)
        pizza = random.choice(pizzas)

        total_sales = random.randint(int(user.get_capacity() / 2), user.get_capacity())
        total_profit = total_sales * (data["pizza"]["types"][pizza]["price"] + user.get_booster_type_total("work"))

        body = "Great Job, you sold quite a few items in your company!\n\n__**Sold Items**__\n"
        body += f"`x{total_sales}` —  {data['pizza']['types'][pizza]['emote']} **{data['pizza']['types'][pizza]['name']}**\n"

        for y in pizzas[:10]:
            if not y == pizza:
                if random.randint(1, 100) < 30:
                    sales = random.randint(int(user.company.get_capacity() / 3), user.company.get_capacity())

                    body += f"`x{sales}` —  {data['pizza']['types'][y]['emote']} **{data['pizza']['types'][y]['name']}**\n"
                    total_profit += sales * data['pizza']['types'][y]['price']
                    total_sales += sales


        body += "\n\n━━━━━━━━━━━━━━\n:fork_knife_plate: **Items:** `{t}`\n:dollar: **Earnings:** `${m}`".format(
            m=helper.money(total_profit), t=helper.money(total_sales))

        user.add_exp(random.randint(1, 10))
        user.add_money(total_profit)
        user.add_total_sold(total_sales)

        user.company.add_money(total_profit)
        user.company.add_total_sold(total_sales)
        user.statistics.add_work(1)

        return await message.reply(
            embed=helper.embed(message, "{e} Overtime Completed!".format(e=random.choice(data["commands"]["emotes"]["work"])),
                               body.format(p=prefix, c=helper.money(total_profit), t=helper.money(total_sales))))


commands.append(Command())
