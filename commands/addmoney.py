import random, asyncio

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "addmoney"
        self.cmd = ["addmon"]
        self.args = True
        self.help = "[mention] [amount]"
        self.category = "Admin"
        self.description = "Adds or remove money from the mention"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 30)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        user_receive = helper.clean_message(clean[0])
        if not db.Exist("users", "id", user_receive):
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['red_alert']} Profile Lookup {data['emotes']['red_alert']}",
                                   f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

        user_receive = UserData(user_receive)

        try:
            value = int(clean[1])
        except:
            return await message.reply(
                embed=helper.embed(message,
                                   f"{data['emotes']['red_alert']} Add/Remove Money {data['emotes']['red_alert']}",
                                   f":x: Please enter a valid amount to add/remove from the user!"))

        user_receive.add_money(value)
        return await message.reply(
            embed=helper.embed(message,
                               f"{data['emotes']['red_alert']} Add/Remove Money {data['emotes']['red_alert']}",
                               f"You have given **{user_receive.get_name()}** :dollar: `${helper.money(value)}`!"))



commands.append(Command())
