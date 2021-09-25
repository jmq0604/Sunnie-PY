import asyncio
import random

import config

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "tips"
        self.cmd = ["t", "tip"]
        self.args = False
        self.help = ""
        self.cooldown = 300
        self.category = "Basic"
        self.description = "Play a mini-game to gather tips from the customers"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        if user.settings.get_interaction():
            random.shuffle(words)

            random_three = words[:4]
            random_three_shuffled = []
            for x in range(len(random_three)):
                str_v = list(random_three[x])
                random.shuffle(str_v)
                random_three_shuffled.append(''.join(str_v))

            orders = ""
            for x in user.get_modules():
                if x == "pizza":
                    orders += "You have **{x} seconds** to try to **unscramble any** of these words:\n\n".format(x=20 + user.get_total_upgrade("tipstime"))

                    for y in range(len(random_three_shuffled)):
                        orders += "`{y}` ".format(y=random_three_shuffled[y])

            embed = helper.embed(message, "Tips Scramble", orders)
            await message.reply(embed=embed)

            def check(m):
                if m.author.id == message.author.id:
                    return True
                return False

            try:
                msg = await client.wait_for('message', check=check, timeout=20 + user.get_total_upgrade("tipstime"))
                user.statistics.add_tips(1)

                answer = helper.clean_message(msg.content).lower()
                if answer in random_three:

                    reward = config.tips_earnings + int(config.tips_earnings * float(user.get_upgrade_effect("tip")) / 100)
                    reward = random.randint(int(reward/2), reward)

                    user.add_money(reward)
                    user.add_exp(random.randint(1, 50))
                    return await msg.reply(
                        embed=helper.embed(message, "{e} Tips Completed".format(e=data["emotes"]["tick"]), "Well done! Your customers were **impressed** by your unscrambling skills that they tipped you :dollar: `${e}`. Keep it up".format(e=reward), footer="Balance: ${s}".format(s=helper.money(user.get_money()))))
                else:
                    return await msg.reply(
                        embed=helper.embed(message, "{e} Tips Incompleted".format(e=data["emotes"]["cross"]), "Your skills at unscrambling was **so terrible**, people started to **leave your restaurant**. Keep it up", footer="Balance: ${s}".format(s=helper.money(user.get_money()) )))

            except asyncio.TimeoutError:
                return await message.reply(
                    embed=helper.embed(message, ":x: Tips Incomplete", "You ran out of time! Better luck next time, your customers left.".format(p=prefix)))
        else:

            reward = config.tips_earnings + int(config.tips_earnings * float(user.get_upgrade_effect("tip")) / 100)
            reward = random.randint(int(reward / 2), reward)

            user.add_exp(random.randint(1, 25))
            user.add_money(reward)

            return await message.reply(
                embed=helper.embed(message, "Tips Collected".format(e=data["emotes"]["cross"]),
                                   f"**{user.get_name()}** has collected :dollar: `${helper.money(reward)}` in tips!",
                                   footer="Balance: ${s}".format(s=helper.money(user.get_money()))))


commands.append(Command())
