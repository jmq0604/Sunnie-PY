import asyncio
import random

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper
from others import mini_games


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "clear"
        self.cmd = ["c"]
        self.args = False
        self.help = ""
        self.category = "Shop"
        self.description = "Sells and clears all your ingredients in your storage"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user=UserData()):
        user_ing = user.get_ingredient()
        prefix = user.get_prefix()

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        try:

            current_storage = user.get_storage()
            await message.reply( embed=helper.embed(message, ":warning: Storage Clearing In-Progress", f"Please reply with a `yes` if you like to **sell out all** the `x{helper.money(current_storage)}` ingredients in your storage!"))
            msg = await client.wait_for('message', check=check, timeout=30)

            ans = helper.clean_message(msg.content).lower().strip()
            if ans == "yes" or ans == "y":

                total_earn = 0
                for x in user_ing:
                    quantity = user.get_total_ingredient(x)
                    sell_price = int(data["pizza"]["ingredients"][x]["price"] / 2 * quantity)
                    total_earn += sell_price

                    user.add_money(sell_price)
                    user.remove_ingredient(x, quantity)

                return await message.reply(embed=helper.embed(message, "{e} Store Cleared".format(e=data["emotes"]["tick"]), f"You sold a total of `x{helper.money(current_storage)}` ingredients for a sum of :dollar: `${helper.money(total_earn)}`!"))
            else:
                return await message.reply(
                    embed=helper.embed(message, ":x: Storage Clearing Failed",
                                       "Clearing of storage has been canceled!"))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Storage Clearing Failed",
                                   "You ran out of time! Please respond next time!".format(
                                       p=prefix)))


commands.append(Command())
