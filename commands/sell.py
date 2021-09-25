from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "sell"
        self.cmd = ["h"]
        self.args = True
        self.help = "[id] <quantity>"
        self.category = "Shop"
        self.description = "Sells items in your inventory or storage"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):

        id = str(clean[0]).lower()
        quantity = 1
        if id in data["items"]:
            user_inv = user.get_inventory()
            if id not in user_inv:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You **do not own** that item!".format(
                        e=data["emotes"]["cross"])))

            if not data["items"][id]["sell_able"]:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} That item is not **sellable**!".format(
                        e=data["emotes"]["cross"])))

            if len(clean) > 1:
                try:
                    if str(clean[0]).lower() in data["others"]["everything"]:
                        quantity = user.get_total_inventory(id)
                    else:
                        quantity = int(clean[1])
                        if quantity < 1:
                            quantity = 1
                except:
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} Please enter a **valid** quantity!".format(
                            e=data["emotes"]["cross"])))

            if user.get_total_inventory(id) < quantity:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You **do not have** that many items to sell!".format(
                        e=data["emotes"]["cross"])))

            sell_price = int(data["items"][id]["price"] / 2 * quantity)
            user.add_money(sell_price)
            user.remove_inventory(id, quantity)

            return await message.reply(
                embed=helper.embed(message, "  ", "You have sold **x{q}** {ee} **{n}** for :dollar: `${s}`".format(
                    n=data["items"][id]["name"], s=helper.money(sell_price), q=quantity, ee=data["items"][id]["emote"])))

        elif id in data["pizza"]["ingredients"]:
            user_inv = user.get_ingredient()
            if id not in user_inv:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You **do not own** that ingredient!".format(
                        e=data["emotes"]["cross"])))

            if len(clean) > 1:
                try:
                    if str(clean[0]).lower() in data["others"]["everything"]:
                        quantity = user.get_total_ingredient(id)
                    else:
                        quantity = int(clean[1])
                        if quantity < 1:
                            quantity = 1
                except:
                    return await message.reply(
                        embed=helper.embed(message, "", "{e} Please enter a **valid** quantity!".format(
                            e=data["emotes"]["cross"])))

            if user.get_total_ingredient(id) < quantity:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You **do not have** that many items to sell!".format(
                        e=data["emotes"]["cross"])))

            sell_price = int(data["pizza"]["ingredients"][id]["price"] / 2 * quantity)
            user.add_money(sell_price)
            user.remove_ingredient(id, quantity)

            return await message.reply(
                embed=helper.embed(message, "", "You have sold **x{q}** {ee} **{n}** for `${s}`".format(
                    n=data["pizza"]["ingredients"][id]["name"], s=helper.money(sell_price), q=helper.money(quantity),
                    ee=data["pizza"]["ingredients"][id]["emote"])))
        else:
            return await message.reply(
                embed=helper.embed(message, "", "{e} That item does not exist!".format(
                    e=data["emotes"]["cross"])))



commands.append(Command())
