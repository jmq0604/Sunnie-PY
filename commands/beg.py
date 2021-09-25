import random

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "beg"
        self.cmd = ["w", "ask", "pray"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Go to the street to beg for money"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 30)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        reward = random.randint(1, 50)

        user.add_exp(random.randint(1, 3))
        name = random.choice(list(data['commands']['beg'].keys()))
        quote = random.choice(data['commands']['beg'][name]['quotes']).lower()

        return await message.reply(embed=helper.embed(message, "Begging", f"A generous passer-by, **{name}**, threw :dollar: `${helper.money(reward)}` at you and said {quote}"))


commands.append(Command())
