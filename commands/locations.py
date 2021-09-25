import math

from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "location"
        self.cmd = ["l", "place", "rent", 'locations']
        self.args = False
        self.help = "<place>"
        self.category = "Expand"
        self.description = "Shows all the different locations available for renting"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        embeds = {}
        prefix = user.get_prefix()
        start_item = 0

        page = 1
        if len(clean) > 0 and not str(clean[0]).isdigit():
            location = str(clean[0])
            if not location in data["location"]:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} That location does not exist for rental!".format(
                        e=data["emotes"]["cross"])))

            if user.get_money() < data["location"][location]["cost"]:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You do not have enough cash!".format(
                        e=data["emotes"]["cross"])))

            if user.get_revenue() < data["location"][location]["rent"]:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You do not meet the income required to rent this place!".format(
                        e=data["emotes"]["cross"])))

            if data["location"][user.get_location()]["level"] >= data["location"][location]["level"]:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} You have already rented this place in the past!".format(
                                           e=data["emotes"]["cross"])))

            user.deduct_money(data["location"][location]["cost"])
            user.set_location(location)
            return await message.reply(embed=helper.embed(message, "{e} Rental Purchased!".format(e=data["emotes"]["tick"]),
                                                          "You have rented out the **{p}**, your max job limit has been increased!".format(p=data["location"][location]["name"])))
        else:
            if len(clean) > 0 and str(clean[0]).isdigit():
                page = (int(clean[0]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[0]) - 1))
                page += 1

            item_displayed = 0
            locations = user.get_available_location()

            total_pages = math.ceil(float(len(locations)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            for x in locations:
                if start_item == 0:
                    embeds["{em} **{e}**".format(e=data["location"][x]["name"], em=data["location"][x]["emote"])] = "Cost: `${c}`\nRent: `${rent}/hr`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏ ‎".format(rent=helper.money(data["location"][x]["rent"]),c=helper.money(data["location"][x]["cost"]), d=data["location"][x]["description"], id=x)
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\n{e} **Balance:** ${b}\nUse `{p}rent [id]` to **rent** a place!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "Rental Places | Page {page}/{total_pages}".format(total_pages=total_pages, page=page), "", embeds=embeds, footer="Use `{p}location <page no>` to view other pages".format(p=prefix))
            await message.reply(embed=embed)


commands.append(Command())
