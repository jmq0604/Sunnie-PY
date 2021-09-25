import asyncio
import discord
import random

from classes import base_command
from classes.user import *
from globals import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "coinflip"
        self.cmd = ["cf", "coin"]
        self.args = True
        self.help = "[head/tail] [amount]"
        self.category = "Gambling"
        self.description = "Plays a coinflip game with the bot"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 10)

    async def run(self, client, message, clean, user=UserData()):

        money = user.get_money()
        bet_amount = user.get_level() * 1000

        if str(clean[0]).find("f") > -1:
            user_flip = 0
        elif str(clean[0]).find("h") > -1:
            user_flip = 1
        else:
            return await message.reply(
                embed=helper.embed(message, f"Coinflip | {message.author.name}",
                                   f"Please choose `heads` or `tails` next time!"))

        if len(clean) > 1:
            try:
                user_number = str(clean[1])
                user_number = re.sub('\D', '', user_number)
                bet_amount = int(user_number)
            except:
                bet_amount = user.get_level() * 1000

        if bet_amount < data["gambling"]["data"]["min_bet"]:
            return await message.reply(
                embed=helper.embed(message, f"Coinflip | {message.author.name}",
                                   f"You are not able to bet lower than `${helper.money(data['gambling']['data']['min_bet'])}`!"))

        if bet_amount > user.get_level() * 1000:
            return await message.reply(
                embed=helper.embed(message, f"Coinflip | {message.author.name}",
                                   "You are **not high leveled enough** to gamble that much! Please **level up** next time!"))

        if money < bet_amount:
            return await message.reply(
                embed=helper.embed(message, f"Coinflip | {message.author.name}", f"You **do not** have enough money to gamble! You need at least `${bet_amount}` to gamble!"))

        bot_flip = random.randint(0, 1)
        flip_data = data['gambling']['coinfilp']
        msg = await message.reply(
            embed=helper.embed(message, f"Coinflip | {message.author.name}",
                               f"", embeds={f"You": f"{flip_data[str(user_flip)]}", "Sunnie ": f"{flip_data['flip']}"}, inline=True))

        await asyncio.sleep(3)

        reward = int(bet_amount * random.uniform(0.1, 2.0))
        end_results = ""

        user.add_exp(random.randint(1, 5))
        if bot_flip == user_flip:
            user.add_money(reward)
            user.statistics.add_gambling_won(reward)
            end_results = f"You **WON** :dollar: `${helper.money(reward)}`"
        elif bot_flip != user_flip:
            user.deduct_money(bet_amount)
            user.statistics.add_gambling_lost(bet_amount)
            end_results = f"You **LOST** :dollar: `${helper.money(bet_amount)}`"

        embed = discord.Embed(title=f"Coinflip | {message.author.name}", description=f"", color=discord.Colour.random())
        embed.add_field(name=f"You", value=f"{flip_data[str(user_flip)]}", inline=True)
        embed.add_field(name="Sunnie ", value=f"{flip_data[str(bot_flip)]}", inline=True)
        embed.add_field(name=f"End Results:", value=end_results, inline=False)

        await msg.edit(embed=embed)


commands.append(Command())
