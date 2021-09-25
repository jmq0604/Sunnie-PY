from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "food"
        self.cmd = ["recipe", "recipes", "cookbook", "book", "r", "pizza"]
        self.args = False
        self.help = "<page no>"
        self.category = "Shop"
        self.description = ""

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 1)

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
        for x in data["pizza"]["types"]:
            if start_item == 0:

                locked = ":lock:"
                for y in user.get_pizza():
                    if y == x:
                        locked = ":unlock:"

                embeds["{em} **{e}** | {lock}".format(lock=locked, e=data["pizza"]["types"][x]["name"], em=data["pizza"]["types"][x]["emote"])] = "Cost: `${c}`\nRecipe: `{r}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏ ‎".format(c=helper.money(data["pizza"]["types"][x]["price"]), id=x, r=helper.list_menu(data["pizza"]["types"][x]["ingredients"]))
                item_displayed += 1
            else:
                start_item -= 1

            if item_displayed == config.items_per_page:
                break

        if len(list(embeds.keys())) > 0:
            embeds[list(embeds.keys())[-1]] += "━━━━━━━━━━━━━━\nUse `{p}work` to **start** working!\nUse `{p}upgrade` to **add more food** item into your menu!"\
                .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

        embed = helper.embed(message, "Cook Book | Page {page}".format(page=page), "".format(p=prefix), embeds=embeds, footer="Use `{p}recipe <page no>` to view other pages".format(p=prefix))
        await message.reply(embed=embed)


commands.append(Command())
