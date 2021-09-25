import config
import math

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "inventory"
        self.cmd = ["inv"]
        self.args = False
        self.help = "<page no>"
        self.category = "Shop"
        self.description = "Shows what you have in your inventory"

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
        user_inv = user.get_inventory()

        total_pages = math.ceil(float(len(user_inv)) / float(config.items_per_page))
        if total_pages == 0:
            total_pages += 1

        for x in user_inv:
            if start_item == 0:
                embeds["{em} **{e}** (x{t})".format(t=user.get_total_inventory(x), e=data["items"][x]["name"], em=data["items"][x]["emote"])] = "Type: `{t}`\nID: `{id}`\n".format(id=x,  t=data["items"][x]["item_type"])
                item_displayed += 1
            else:
                start_item -= 1

            if item_displayed == config.items_per_page:
                break

        embed = helper.embed(message, "{name}'s Inventory | Page {page}/{total_pages}".format(total_pages=total_pages, page=page, name=message.author.name), "", embeds=embeds, footer="Use `{p}inv <page no>` to view other pages".format(p=prefix))
        await message.reply(embed=embed)




commands.append(Command())
