import config
import math

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "storage"
        self.cmd = ["stock", "holding", "st"]
        self.args = False
        self.help = "<page no>"
        self.category = "Shop"
        self.description = "Shows all your ingredients that you have"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()
        embeds = {}
        start_item = 0

        page = 1
        if len(clean) > 0 and str(clean[0]).isdigit():
            page = (int(clean[0]) - 1)
            if page > 0:
                start_item = int(config.items_per_page * (int(clean[0]) - 1))
            page += 1

        item_displayed = 0
        user_inv = user.get_ingredient()
        
        total_pages = math.ceil(float(len(user_inv)) / float(config.items_per_page))
        if total_pages == 0:
            total_pages += 1

        for x in user_inv:
            if start_item == 0:
                embeds["{em} **{e}** (x{t})".format(t=user.get_total_ingredient(x), e=data["pizza"]["ingredients"][x]["name"], em=data["pizza"]["ingredients"][x]["emote"])] = "**type**: `{t}`\n**id**: `{id}`\n".format(id=x, t=data["pizza"]["ingredients"][x]["type"])
                item_displayed += 1
            else:
                start_item -= 1

            if item_displayed == config.items_per_page:
                break

        if len(list(embeds.keys())) > 0:
            embeds[list(embeds.keys())[
                -1]] += "\n━━━━━━━━━━━━━━\nUse `{p}ingredients` to **view** available ingredient!\nUse `{p}sell [id] [quantity]` to **sell** your ingredients!" \
                .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

        embed = helper.embed(message, "Storage | Page {page}/{total_pages} - Storage: {s}/{ms}".format(total_pages=total_pages, s=user.get_storage(), ms=user.get_max_storage(), page=page, name=message.author.name), "", embeds=embeds, footer="Use `{p}storage <page no>` to view other pages".format(p=prefix))
        await message.reply(embed=embed)




commands.append(Command())
