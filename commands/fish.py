import config
import random, asyncio
import time

from classes import user
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "fish"
        self.cmd = ["fi", "fishing"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Uses your fishing skills to go and fish"

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

        pharse = random.choice(data['skills'][self.name]['pharses'])
        reply = await message.reply(embed=helper.embed(message, f"Get Ready....", "*You ready your fishing rod.....*", footer=" "))
        await asyncio.sleep(random.randint(2, 5))

        await reply.edit(embed=helper.embed(message, "Get Ready....", F"TYPE `{pharse}` NOW!", footer=" "))

        try:
            msg = await client.wait_for('message', check=check, timeout=5)

            if helper.clean_message(msg.content).lower().strip() == pharse.lower():
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
                    embed=helper.embed(message, "{e} Fishing Success".format(e=data["emotes"]["tick"]),
                                       f"**Here is what you caught:**\n\n{body}", footer=" "))

            else:
                return await msg.reply(embed=helper.embed(message, ":x: Fishing Failed", "You somehow **performed the wrong action** and the fish got away!", footer=" "))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Fishing Failed",
                                   "Type the phrase faster next time, the fish **got away**!", footer=" "))


commands.append(Command())
