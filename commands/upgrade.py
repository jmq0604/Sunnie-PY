import math
import random

from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "upgrade"
        self.cmd = ["u", "upgrades", "up"]
        self.args = False
        self.help = "[upgrade id]"
        self.category = "Expand"
        self.description = "Shows everything you can upgrade in your pizzeria"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        if len(clean) > 0 and not str(clean[0]).isdigit():
            upgrades = user.get_available_upgrade()
            id = str(clean[0]).lower()

            if id not in upgrades:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} That upgrade does not exist or you have not unlocked it yet!".format(
                        e=data["emotes"]["cross"])))

            if user.get_money() < user.get_upgrade_price(id):
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You do not have enough money to purchase this upgrade!".format(
                        e=data["emotes"]["cross"])))

            effects = user.get_upgrade_effect(id, True)
            price = user.get_upgrade_price(id)
            user.add_upgrade(id)
            user.deduct_money(price)

            body = "You have just upgraded your **{u}**!".format(u=data["upgrades"][id]["name"])
            if id == "oven":
                all_types = list(data["pizza"]["types"])
                already_owned = []
                for x in user.get_pizza():
                    already_owned.append(x)

                random.shuffle(all_types)
                for x in all_types:
                    if x not in already_owned:
                        user.add_pizza(x)

                        return await message.reply(
                            embed=helper.embed(message, "",
                                               "You have just unlocked a **brand new food item**, the {e} **{n}**!".format(
                                                   e=data["pizza"]["types"][x]["emote"], n=data["pizza"]["types"][x]["name"])))

                body = ":unlock: You have fully **unlocked every food item** there are! Good job!".format(r=data["emotes"]["running"])
            elif id == "storage":
                user.add_max_storage(effects)
                body = "You have just added **{r}** to your storage space, enjoy the new area!".format(r=effects)
            elif id == "furniture":
                user.add_capacity(effects)
                body = "You have just added **{r}** to your capacity, enjoy the new customers!".format(r=effects)
            elif data["upgrades"][id]["increase"] == "capacity":
                user.add_modules_capacity(data["upgrades"][id]["module"], effects)
                body = f"You have just added **{effects}** to your capacity, enjoy the new customers in your {data['upgrades'][id]['module']}!"

            user.add_exp(random.randint(1, 50))
            return await message.reply(embed=helper.embed(message, "{e} Purchased!".format(e=data["emotes"]["tick"]), body))
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

            upgrades = user.get_available_upgrade()
            total_pages = math.ceil(float(len(upgrades)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            for x in upgrades:
                if start_item == 0:
                    embeds["{e} {n} - {s}".format(s=user.get_total_upgrade(x), e=data["upgrades"][x]["emote"], n=data["upgrades"][x]["name"])] = "Info: `{i}`\nPrice: `${p}`\nEffects: `{e}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏‎ "\
                        .format(i=data["upgrades"][x]["info"], id=x, p=helper.money(user.get_upgrade_price(x)), e=data["upgrades"][x]["format"].format(e=helper.money(user.get_upgrade_effect(x, True))))
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\n{e} **Balance:** ${b}\nUse `{p}upgrade [upgrade id]` to **purchase** an upgrade!\nUse `{p}upgrade [page]` to **view** different pages!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "{e} Upgrade Shop | Page {page}/{total_pages}".format(total_pages=total_pages, page=page, e=data["emotes"]["star"]), "",
                                 embeds=embeds)

            await message.reply(embed=embed)


commands.append(Command())
