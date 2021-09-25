import random, asyncio, time

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "forcestart"
        self.cmd = ["force", "forceadd", "forcefound"]
        self.args = True
        self.help = "[mention]"
        self.category = "Admin"
        self.description = "Forcefully starts someone's restaurant"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 30)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        user_receive = helper.clean_message(clean[0])
        if db.Exist("users", "id", user_receive):
            return await message.reply(
                embed=helper.embed(message, f"Profile Lookup",
                                   f":x: That person **already exist** in the database!"))

        db.Retrieve("users", "id", str(user_receive))
        db.Update("users", "clean_time", str(round(time.time())), str(user_receive))

        user_receive = UserData(user_receive)
        pizza = list(data["pizza"]["types"].keys())[0]

        user_receive.add_pizza(pizza)
        user_receive.add_modules("pizza")

        return await message.reply(
            embed=helper.embed(message, f"{data['emotes']['red_alert']} ADDED TO DATABSE {data['emotes']['red_alert']}",
                               "That person has **been added** to the database!".format(
                                   p=prefix)))

commands.append(Command())
