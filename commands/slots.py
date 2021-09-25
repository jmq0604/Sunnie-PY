import asyncio
import discord
import random

from classes import base_command
from classes.user import *
from globals import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "slots"
        self.cmd = ["slot", "sl", "spin"]
        self.args = False
        self.help = "[amount]"
        self.category = "Gambling"
        self.description = "Plays a slot machine"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 10)

    async def run(self, client, message, clean, user=UserData()):

        money = user.get_money()
        bet_amount = user.get_level() * 1000

        if len(clean) > 0:
            try:
                user_number = str(clean[0])
                user_number = re.sub('\D', '', user_number)
                bet_amount = int(user_number)
            except:
                bet_amount = user.get_level() * 1000

        if bet_amount < data["gambling"]["data"]["min_bet"]:
            return await message.reply(
                embed=helper.embed(message, f"Slots | {message.author.name}",
                                   f"You are not able to bet lower than `${helper.money(data['gambling']['data']['min_bet'])}`!"))

        if bet_amount > user.get_level() * 1000:
            return await message.reply(
                embed=helper.embed(message, f"Slots | {message.author.name}",
                                   "You are **not high leveled enough** to gamble that much! Please **level up** next time!"))

        if money < bet_amount:
            return await message.reply(
                embed=helper.embed(message, f"Slots | {message.author.name}", f"You **do not** have enough money to gamble! You need at least `${bet_amount}` to gamble!"))


        slot_data = data['gambling']['slots']
        msg = await message.reply(
            embed=helper.embed(message, f"Slots | {message.author.name}",
                               f"", embeds={"Spinning": f"{slot_data['spin']}|{slot_data['spin']}|{slot_data['spin']}\n\n**Bet: `${helper.money(bet_amount)}`**"}, inline=True, footer=" "))

        await asyncio.sleep(3)

        slots = []
        profit = 0

        for x in range(3):
            slot = random.choice(list(slot_data["fruits"].keys()))
            if slot in slots:
                profit += slot_data['fruits'][slot]['profit']

            slots.append(slot)

        earnings = int(bet_amount * (profit / 100.0))
        if profit:
            user.add_money(earnings)
            user.statistics.add_gambling_won(earnings)
            body = f"**You won** :dollar: `${helper.money(earnings)}`"
        else:
            user.deduct_money(bet_amount)
            user.statistics.add_gambling_lost(bet_amount)
            body = f"**Better luck next time!**"

        return await msg.edit(embed=helper.embed(message, f"Slots | {message.author.name}",
                               f"", embeds={"Spinned": f"{slot_data['fruits'][slots[0]]['emote']}|{slot_data['fruits'][slots[1]]['emote']}|{slot_data['fruits'][slots[2]]['emote']}\n\n{body}"}, inline=True, footer=" "))



commands.append(Command())
