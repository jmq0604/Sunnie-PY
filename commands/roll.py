import asyncio
import discord
import random

from classes import base_command
from classes.user import *
from globals import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "roll"
        self.cmd = ["rolling", "ro"]
        self.args = False
        self.help = "[amount]"
        self.category = "Gambling"
        self.description = "Plays a simple dice game with the bot"

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
                embed=helper.embed(message, f"Rolling | {message.author.name}",
                                   f"You are not able to bet lower than `${helper.money(data['gambling']['data']['min_bet'])}`!"))

        if bet_amount > user.get_level() * 1000:
            return await message.reply(
                embed=helper.embed(message, f"Rolling | {message.author.name}",
                                   "You are **not high leveled enough** to gamble that much! Please **level up** next time!"))

        if money < bet_amount:
            return await message.reply(
                embed=helper.embed(message, f"Rolling | {message.author.name}", f"You **do not** have enough money to gamble! You need at least `${bet_amount}` to gamble!"))

        user_roll = random.randint(1, 12)
        bot_roll = random.randint(1, 12)

        msg = await message.reply(
            embed=helper.embed(message, f"Rolling | {message.author.name}",
                               f"", embeds={f"You": f"`...`", "Sunnie ": f"`...`"}, inline=True))

        await asyncio.sleep(3)

        reward = int(bet_amount * random.uniform(0.1, 2.0))
        user.add_exp(random.randint(1, 5))

        if user_roll > bot_roll:
            user.add_money(reward)
            user.statistics.add_gambling_won(reward)
            end_results = f"You **WON** :dollar: `${helper.money(reward)}`"
        elif bot_roll > user_roll:
            user.deduct_money(bet_amount)
            user.statistics.add_gambling_lost(bet_amount)
            end_results = f"You **LOST** :dollar: `${helper.money(bet_amount)}`"
        else:
            end_results = "TIE!"

        embed = discord.Embed(title=f"Rolled | {message.author.name}", description=f"", color=discord.Colour.random())
        embed.add_field(name=f"You", value=f":game_die: `{user_roll}`", inline=True)
        embed.add_field(name="Sunnie ", value=f":game_die: `{bot_roll}`", inline=True)
        embed.add_field(name=f"End Results:", value=end_results, inline=False)

        await msg.edit(embed=embed)


commands.append(Command())
