import config
import random, asyncio
import time

from classes import user
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "hunt"
        self.cmd = ["hu", "hunting", "meat"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Going hunting in the forest to gather meat ingredients"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 150)

    async def run(self, client, message, clean, user=user.UserData()):
        prefix = user.get_prefix()

        if user.get_level() < data['skills'][self.name]['level']:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} You **do not meet the required level** to use this skill! Use `{prefix}skills` to check the level requirements".format(
                                                              e=data["emotes"]["cross"], prefix=prefix)))

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        position = random.randint(0, 2)

        gem = ""
        for x in range(3):
            if x == position:
                gem += random.choice(data['skills'][self.name]["animal"])
            else:
                gem += random.choice(data['skills'][self.name]["bush"])

        reply = await message.reply(embed=helper.embed(message, f"Firing Range", f"{gem}\n\n**Select Shooting Position**\n`left` `middle` `right`", footer=" "))

        try:
            msg = await client.wait_for('message', check=check, timeout=5)
            if helper.clean_message(msg.content).lower().strip() in data['skills'][self.name]["position"][0]:
                user_answer = 0
            elif helper.clean_message(msg.content).lower().strip() in data['skills'][self.name]["position"][1]:
                user_answer = 1
            elif helper.clean_message(msg.content).lower().strip() in data['skills'][self.name]["position"][2]:
                user_answer = 2
            else:
                return await message.reply(
                    embed=helper.embed(message, "{e} Hunting Failed".format(e=data["emotes"]["cross"]),
                                       f"Next time choose between the three provided options: `left` `middle` and `right`"))

            if user_answer == position:
                skills = user.get_skill_points(self.name)
                max_items = data['skills'][self.name]['stats']['max_items'] + skills
                max_quantity = data['skills'][self.name]['stats']['max_quantity'] + (skills * 10)
                user.statistics.add_skills(1)

                body = ""
                for x in range(random.randint(1, max_items)):
                    item = random.choice(data['skills'][self.name]["items"])
                    quantity = random.randint(1, max_quantity)
                    user.add_ingredient(item, quantity)
                    body += f"`x{quantity}` —  {data['pizza']['ingredients'][item]['emote']} **{data['pizza']['ingredients'][item]['name']}**\n"

                return await message.reply(
                    embed=helper.embed(message, "{e} Hunting Success".format(e=data["emotes"]["tick"]),
                                       f"**Here is what you caught:**\n\n{body}"))

            else:
                return await msg.reply(embed=helper.embed(message, ":x: Hunting Failed", "You somehow **performed the wrong action** and the animal got away!"))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Hunting Failed",
                                   "Type the phrase faster next time, the animal **got away**!"))


commands.append(Command())
