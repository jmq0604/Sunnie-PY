import math

from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "ingredients"
        self.cmd = ["i"]
        self.args = False
        self.help = "[id/all/pizza id] [quantity]"
        self.category = "Shop"
        self.description = "Lists all the unlocked ingredients or purchase them"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 1)

    async def run(self, client, message, clean, user):
        embeds = {}
        prefix = user.get_prefix()
        start_item = 0

        if len(clean) > 0 and not str(clean[0]).isdigit():
            ingredients_id = []

            if user.get_storage() >= user.get_max_storage():
                return await message.reply(
                    embed=helper.embed(message, "", "{e} Your storage is full!".format(
                        e=data["emotes"]["cross"])))

            single_ingredient = True
            allowed_ingredients = []
            for x in user.get_pizza():
                if x == clean[0].lower():
                    for y in data["pizza"]["types"][x]["ingredients"]:
                        single_ingredient = False
                        ingredients_id.append(y)

                for y in data["pizza"]["types"][x]["ingredients"]:
                    allowed_ingredients.append(y)

            if clean[0] == "all":
                ingredients_id = allowed_ingredients
                single_ingredient = False

            quantity = 1
            if len(clean) > 1:
                try:
                    quantity = int(clean[1])
                except:
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} Please enter a valid quantity!".format(
                            e=data["emotes"]["cross"])))

            if single_ingredient:
                ingredients_id = str(clean[0]).lower()

                found = False
                for x in data["pizza"]["ingredients"]:
                    if x in ingredients_id:
                        if ingredients_id in allowed_ingredients or data["pizza"]["ingredients"][x]["type"] == "optional":
                            found = True

                if not found:
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} That ingredient does not exist or you have not unlocked it yet!".format(
                            e=data["emotes"]["cross"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))

                if user.get_money() < data["pizza"]["ingredients"][ingredients_id]["price"] * quantity:
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} You do not have enough **cash** for this ingredient!".format(
                            e=data["emotes"]["cross"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))

                if user.get_storage() + quantity > user.get_max_storage():
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} You can't buy more than what your storage can hold!".format(
                            e=data["emotes"]["cross"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))

                user.deduct_money(data["pizza"]["ingredients"][ingredients_id]["price"] * quantity)
                user.add_ingredient(ingredients_id, quantity)
                return await message.reply(embed=helper.embed(message, "{e} Purchased!".format(e=data["emotes"]["tick"]),
                                                              "You have purchased **x{no}** of **{n}**! Costing you :dollar: `${cost}`".format(cost=helper.money(data["pizza"]["ingredients"][ingredients_id]["price"] * quantity),
                                                                  no=quantity, n=data["pizza"]["ingredients"][ingredients_id]["name"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))
            else:
                total_quantity = quantity * len(ingredients_id)
                if user.get_storage() + total_quantity > user.get_max_storage():
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} You can't buy more than what your storage can hold!".format(
                                               e=data["emotes"]["cross"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))

                total_price = 0
                for x in ingredients_id:
                    total_price += data["pizza"]["ingredients"][x]["price"] * quantity

                if user.get_money() < total_price:
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} You do not have enough **cash** for these ingredients!".format(
                                               e=data["emotes"]["cross"]), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))

                body = "You have purchased a total of **x{no}** items:\n"
                user.deduct_money(total_price)
                for x in ingredients_id:
                    user.add_ingredient(x, quantity)
                    body += "`x{c}` —  {e} **{n}**\n".format(c=quantity, e=data["pizza"]["ingredients"][x]["emote"], n=data["pizza"]["ingredients"][x]["name"])

                body += "\nCost: `${cost}`".format(cost=helper.money(total_price))

                return await message.reply(embed=helper.embed(message, "{e} Purchased!".format(e=data["emotes"]["tick"]),body.format(no=total_quantity),
                                 footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))
        else:
            page = 1
            if len(clean) > 0 and str(clean[0]).isdigit():
                page = (int(clean[0]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[0]) - 1))
                page += 1

            allowed_ingredients = []
            for x in user.get_pizza():
                for y in data["pizza"]["types"][x]["ingredients"]:
                    allowed_ingredients.append(y)

            ingredients = user.get_available_ingredients()

            total_pages = math.ceil(float(len(ingredients)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            item_displayed = 0
            for x in ingredients:
                if start_item == 0:
                        embeds["{em} **{e}** - x{t}".format(t=user.get_total_ingredient(x),
                                                            e=data["pizza"]["ingredients"][x]["name"],
                                                            em=data["pizza"]["ingredients"][x][
                                                                "emote"])] = "Price: `${p}`\nType: `{t}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏‎ ".format(
                            t=data["pizza"]["ingredients"][x]["type"], id=x, p=helper.money(data["pizza"]["ingredients"][x]["price"]))
                        item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\n{e} **Balance:** ${b}\nUse `{p}ingredients [id/all/pizza id] [quantity]` to **purchase** an ingredient!\nUse `{p}storage` to **view** your storage!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "Ingredients Shop | Page {page}/{total_pages}".format(page=page, total_pages=total_pages),
                                 "".format(
                                     p=prefix), embeds=embeds,
                                 footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage()))
            await message.reply(embed=embed)


commands.append(Command())
