import config
import random, asyncio
import time

from classes import user
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "harvest"
        self.cmd = ["ha", "yield", "produce"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Harvests your small home grown garden for ingredients"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 300)

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

        random.shuffle(words)
        hidden_ingredients = list(data['pizza']["ingredients"].keys())

        chosen = random.randint(0, 2)
        hidden_words = words[:3]
        hidden_ingredients = hidden_ingredients[:3]

        hidden_body = ""
        for x in range(3):
            hidden_body += f"{data['pizza']['ingredients'][hidden_ingredients[x]]['emote']} - `{hidden_words[x]}`\n"

        reply = await message.reply(
            embed=helper.embed(message, f"Memorize Harvesting", hidden_body, footer=" "))

        await asyncio.sleep(7)

        await reply.edit(embed=helper.embed(message, "Memorize Harvesting", f"**What word was beside:**  {data['pizza']['ingredients'][hidden_ingredients[chosen]]['emote']}", footer=" "))

        try:
            msg = await client.wait_for('message', check=check, timeout=5)

            if helper.clean_message(msg.content).lower().strip() == hidden_words[chosen].lower():
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
                    embed=helper.embed(message, "{e} Harvesting Success".format(e=data["emotes"]["tick"]),
                                       f"**Here is what you harvested:**\n\n{body}", footer=" "))

            else:
                return await msg.reply(embed=helper.embed(message, ":x: Harvesting Failed",
                                                          f"You somehow **got the word wrong**, the right word was `{hidden_words[chosen].lower()}`", footer=" "))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Harvesting Failed",
                                   "Type the phrase faster next time, the plants **grew bad**!", footer=" "))


commands.append(Command())
