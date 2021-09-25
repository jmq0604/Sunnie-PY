import config
import random
import time

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "daily"
        self.cmd = ["d"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Claim your daily bonus"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):

        if time.time() - user.get_daily_time() > config.daily_cooldown:
            user.reset_daily_time()

            max_items = 2
            if user.get_daily_amount() >= 7:
                max_items = 6
                user.deduct_daily_amount(user.get_daily_amount())

            lootboxes = random.randint(1, max_items)
            boost = random.randint(1, 2)
            cash_earn = random.randint(18000, 20000 * (max_items / 2))

            user.add_exp(random.randint(250, 500))
            user.add_money(cash_earn)
            user.add_inventory("lootbox", lootboxes)
            user.add_inventory("daily", boost)

            body = "You have claimed your **${cash}** reward!\n\n__**You have Claimed the following:**__\n`x{c}` —  {e} **{n}**\n`x{cm}` —  {em} **{nm}**\n\n"\
                .format(cm=boost, em=data["items"]["daily"]["emote"], nm=data["items"]["daily"]["name"], c=lootboxes, e=data["items"]["lootbox"]["emote"], n=data["items"]["lootbox"]["name"], cash=helper.money(cash_earn))

            body += "__**Daily Streak Progress**__\n"
            for x in range(7):
                if x > (user.get_daily_amount() - 1):
                    body += data["emotes"]["b_pizza"]
                else:
                    body += data["emotes"]["a_pizza"]

            user.add_daily_amount(1)
            return await message.reply(embed=helper.embed(message, "Daily Claims", body))
        else:

            body = "You have already claimed your reward! You have **{t}** left before you can claim again\n\n".format(t=helper.time_remaining(int(time.time() - user.get_daily_time()), config.daily_cooldown))

            body += "__**Daily Streak Progress**__\n"
            for x in range(7):
                if x > (user.get_daily_amount() - 1):
                    body += data["emotes"]["b_pizza"]
                else:
                    body += data["emotes"]["a_pizza"]

            return await message.reply(
                embed=helper.embed(message, "Daily Claims", body))



commands.append(Command())
