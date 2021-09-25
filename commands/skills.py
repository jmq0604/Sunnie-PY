import math
import random

from classes import user
from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "skills"
        self.cmd = ["sk", "skill", "level", "levels"]
        self.args = False
        self.help = "[skill id]"
        self.category = "Expand"
        self.description = "Shows your skill points and what you can use it on"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2)

    async def run(self, client, message, clean, user=user.UserData()):
        prefix = user.get_prefix()

        if len(clean) > 0 and not str(clean[0]).isdigit():
            id = str(clean[0]).lower()

            if id not in data["skills"]:
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} That is **not a valid skill** you can pick!".format(
                                                                  e=data["emotes"]["cross"])))

            if user.get_level() < data['skills'][id]['level']:
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} You **do not meet the required level** to use this skill! Use `{prefix}skills` to check the level requirements".format(
                                                                  e=data["emotes"]["cross"], prefix=prefix)))

            if user.get_unused_skill_points() < 1:
                return await message.reply(embed=helper.embed(message, "",
                                                              "{e} You **do not have enough points to spend**, please level up to get more points!".format(
                                                                  e=data["emotes"]["cross"])))

            user.deduct_unused_skill_points(1)
            user.add_skill_point(id)
            return await message.reply(embed=helper.embed(message, "{e} Skill Upgraded".format(e=data["emotes"]["tick"]),
                                                          f"You just spent your skill points on {data['skills'][id]['emote']} **{data['skills'][id]['name']}** and leveled it up to `{user.get_skill_points(id)}`"))
        else:
            start_item = 0
            page = 1
            if len(clean) > 0 and str(clean[0]).isdigit():
                page = (int(clean[0]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[0]) - 1))
                page += 1

            embeds = {}
            item_displayed = 0

            skills = list(data["skills"].keys())
            total_pages = math.ceil(float(len(skills)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            for x in skills:
                if start_item == 0:
                    locked = user.get_skill_points(x)
                    if user.get_level() < data['skills'][x]['level']:
                        locked = ":lock:"

                    embeds[f"{data['skills'][x]['emote']} {data['skills'][x]['name']} - {locked}"] = f"Required Level: `{data['skills'][x]['level']}`\nID: `{x}`\n‎‎‏‏‎ ‎‏‏‎ "
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\n{e} **Skill Points:** `{b}`\nUse `{p}skills [skill id]` to **use a point** on a skill!\nUse `{p}skills [page]` to **view** different pages!" \
                    .format(e=data["emotes"]["skills"], b=helper.money(user.get_unused_skill_points()), p=prefix)

            embed = helper.embed(message, "{e} Skill Shop | Page {page}/{total_pages}".format(total_pages=total_pages, page=page, e=data["emotes"]["star"]), "",
                                 embeds=embeds)

            await message.reply(embed=embed)


commands.append(Command())
