import time

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "found"
        self.cmd = ["setup", "start", "startup", "register"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Starts up your pizzeria journey"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 300)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        exist = db.Exist("users", "id", str(message.author.id))
        if exist:
            await message.reply(
                embed=helper.embed(message, "", "{e} Your shop has already been setup!".format(e=data["emotes"]["cross"])))
        else:
            db.Retrieve("users", "id", str(message.author.id))
            db.Update("users", "clean_time", str(round(time.time())), str(message.author.id))

            pizza = list(data["pizza"]["types"].keys())[0]

            user.add_pizza(pizza)
            user.add_modules("pizza")
            user.settings.presettings()

            try:
                await message.author.send(embed=helper.embed(message, "<:welcome2:856195655583924265> Welcome to Sunnie Restaurant <:welcome:856195642148782081>", config.help_embed))
                await message.author.send("https://discord.gg/eFF9pS3DRd")
            except:
                return await message.reply(embed=helper.embed(message, "Welcome to the family!",
                                                              "Run `{p}profile` to view your shop! Since you have DM disabled, i am not able to send you the guide, please turn it on and type `{p}tutorial` to receive it once its enabled!".format(
                                                                  e=data["emotes"]["cross"], p=prefix)))

            return await message.reply(embed=helper.embed(message, "Welcome to the family!", "Run `{p}profile` to view your shop! Please check your **DM** to see the guide on how to play!".format(e=data["emotes"]["cross"], p=prefix)))


commands.append(Command())
