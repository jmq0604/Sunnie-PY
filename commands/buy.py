from helper import helper
from classes import base_command

from globals import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "buy"
        self.cmd = ["purchase"]
        self.args = False
        self.help = "[item id] <quantity>"
        self.category = "Shop"
        self.description = "Buy items from the shop and adds it to your inventory"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        if not len(clean):
            for cmd in commands:
                if cmd.name == "shop":
                    return await cmd.run(client, message, clean, user)

        item_id = str(clean[0]).lower()
        if not item_id in data["items"]:
            name_find = None
            if item_id in data["upgrades"]:
                name_find = "upgrade"
            elif item_id in data["pizza"]["ingredients"]:
                name_find = "ingredients"

            if name_find:
                for cmd in commands:
                    if cmd.name == name_find:
                        return await cmd.prerun(client, message, clean, user)

            return await message.reply(
                embed=helper.embed(message, "", "{e} That item does not **exist** in shops!".format(
                    e=data["emotes"]["cross"])))

        if not data["items"][item_id]["in_shop"]:
            return await message.reply(
                embed=helper.embed(message, "", "{e} That item **cannot be bought** right now!".format(
                    e=data["emotes"]["cross"])))

        quantity = 1
        if len(clean) > 1:
            try:
                quantity = int(clean[1])
                if quantity < 1:
                    quantity = 1
            except:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} Please enter a valid quantity!".format(
                        e=data["emotes"]["cross"])))

        if user.get_money() < data["items"][item_id]["price"] * quantity:
            return await message.reply(
                embed=helper.embed(message, "", "{e} You do not have enough **cash** for this item!".format(
                    e=data["emotes"]["cross"])))

        price = data["items"][item_id]["price"] * quantity
        user.deduct_money(price)
        user.add_inventory(item_id, quantity)
        return await message.reply(embed=helper.embed(message, "{e} Purchased!".format(e=data["emotes"]["tick"]),
                                                      "You have purchased **x{no}** of **{n}** {em} for `${ee}`!".format(
                                                          no=quantity, n=data["items"][item_id]["name"],
                                                          em=data["items"][item_id]["emote"], ee=helper.money(price))))


commands.append(Command())
