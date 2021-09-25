import math

from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "shop"
        self.cmd = ["retail", "outlet", "store", "s"]
        self.args = False
        self.help = "<page no>"
        self.category = "Shop"
        self.description = "Shows everything which are sold in the shop"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        embeds = {}
        prefix = user.get_prefix()
        start_item = 0

        page = 1
        if len(clean) > 0 and str(clean[0]).isdigit():
            page = (int(clean[0]) - 1)
            if page > 0:
                start_item = int(config.items_per_page * (int(clean[0]) - 1))
            page += 1

        item_displayed = 0
        shop_items = user.get_available_shop()

        total_pages = math.ceil(float(len(shop_items)) / float(config.items_per_page))
        if total_pages == 0:
            total_pages += 1

        for x in shop_items:
            if start_item == 0:
                embeds["{em} **{e}**".format(e=data["items"][x]["name"], em=data["items"][x]["emote"])] = "{d}\n**Cost:** `${c}`\n**ID:** `{id}`\n".format(c=helper.money(data["items"][x]["price"]), d=data["items"][x]["description"], id=x)
                item_displayed += 1
            else:
                start_item -= 1

            if item_displayed == config.items_per_page:
                break

        if len(list(embeds.keys())) > 0:
            embeds[list(embeds.keys())[-1]] += "━━━━━━━━━━━━━━\n{e} **Balance:** ${b}\nUse `{p}buy [id]` to **purchase** an item!\nUse `{p}inv` to **view** your items!"\
                .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

        embed = helper.embed(message, "Sunnie Industry's Shop | Page {page}/{total_pages}".format(total_pages=total_pages, page=page), "Welcome to the sunnie's shop! You can purchase many goods which are **legal**".format(p=prefix), embeds=embeds, footer="Use `{p}shop <page no>` to view other pages".format(p=prefix))
        await message.reply(embed=embed)


commands.append(Command())
