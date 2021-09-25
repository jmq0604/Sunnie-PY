import asyncio
import random

from classes import base_command
from globals import *
from helper import helper
from others import mini_games


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "use"
        self.cmd = ["y"]
        self.args = True
        self.help = "[tem id]"
        self.category = "Shop"
        self.description = "Use an item in your inventory such as a booster or other items"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):

        id = str(clean[0]).lower()
        user_inv = user.get_inventory()
        if id not in user_inv:
            return await message.reply(
                embed=helper.embed(message, "", "{e} You do not own that item!".format(
                    e=data["emotes"]["cross"]), footer=" "))

        if id not in data["items"]:
            return await message.reply(
                embed=helper.embed(message, "", "{e} That item does not exist!".format(
                    e=data["emotes"]["cross"]), footer=" "))

        if not data["items"][id]["use_able"]:
            return await message.reply(
                embed=helper.embed(message, "", "{e} That item is not usable!".format(
                    e=data["emotes"]["cross"]), footer=" "))

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        if data["items"][id]["item_type"] == "booster":

            if user.get_booster_active(id):
                return await message.reply(
                    embed=helper.embed(message, "", "{e} That boost is **already active**!".format(
                        e=data["emotes"]["cross"])))

            user.remove_inventory(id)
            if data["items"][id]["extra"]["chance"] >= random.randint(0, 100):
                user.add_booster(id, data["items"][id]["extra"]["duration"], data["items"][id]["extra"]["type"], data["items"][id]["extra"]["effect"])
            else:
                return await message.reply(
                    embed=helper.embed(message, "Booster Failed",
                                       random.choice(data["items"][id]["extra"]["fail"])))

            boost = ""
            if data["items"][id]["extra"]["type"] == "percentage":
                boost = "`+{e}%/hr`".format(e=data["items"][id]["extra"]["effect"])
            elif data["items"][id]["extra"]["type"] == "revenue":
                boost = "`+${e}/hr`".format(e=data["items"][id]["extra"]["effect"])
            elif data["items"][id]["extra"]["type"] == "work":
                boost = "`+${e}/pizza`".format(e=data["items"][id]["extra"]["effect"])

            return await message.reply(
                embed=helper.embed(message, "", "You have used an **{n}** and received a {ee} **{e}** boost for **{s}**".format(
                    n=data["items"][id]["name"], e=boost, s=helper.time_human(data["items"][id]["extra"]["duration"]), ee=data["items"][id]['emote'])))
        elif data["items"][id]["item_type"] == "collectable":
            return await message.reply(
                embed=helper.embed(message, data["items"][id]["name"],
                                   f"**{data['items'][id]['description']}**"))
        elif data["items"][id]["item_type"] == "bonus":

            open = 1
            amount = user.get_total_inventory(id)
            if data["items"][id]["extra"]["open_multiple"]:
                if amount > 1:
                    await message.reply(embed=helper.embed(message, "", f"How many **{data['items'][id]['name']}** do you want to open? You currently have `{amount}` unused {data['items'][id]['name']}.", footer=" "))

                    try:
                        msg = await client.wait_for('message', check=check, timeout=30)

                        ans = helper.clean_message(msg.content).lower()
                        ans = ans.strip()

                        if str(ans).isdigit():
                            ans = int(ans)
                            if ans > amount:
                                open = amount
                            else:
                                open = ans

                    except asyncio.TimeoutError:
                        return await message.reply(embed=helper.embed(message, "Learn how to respond next time.", "", footer=" "))

            if open < 1:
                open = amount

            if id == "banknote":
                increase = 0
                for x in range(open):
                    increase += random.randint(1, data['items'][id]['extra']['max_deposit'])

                user.remove_inventory(id, open)
                user.add_bonus_max(increase)

                return await message.reply(
                    embed=helper.embed(message, f"{data['items'][id]['name']} Opened", f"You have opened `x{helper.money(open)}` {data['items'][id]['emote']} {data['items'][id]['name']} and increased your deposit limit by `${helper.money(increase)}`", footer=" "))
            elif id == "lottery":
                increase = 0
                for x in range(open):
                    increase += random.choice(data['items'][id]['extra']['winnings'])

                user.remove_inventory(id, open)
                user.add_money(increase)

                return await message.reply(
                    embed=helper.embed(message, f"{data['items'][id]['name']} Redeemed",
                                       f"You have opened `x{helper.money(open)}` {data['items'][id]['emote']} {data['items'][id]['name']} and won a total of :dollar: `${helper.money(increase)}`",
                                       footer=" "))
            elif id == "golden":
                increase = 0
                for x in range(open):
                    increase += random.choice(data['items'][id]['extra']['winnings'])

                user.remove_inventory(id, open)
                user.add_money(increase)

                return await message.reply(
                    embed=helper.embed(message, f"{data['items'][id]['name']} Redeemed",
                                       f"You have opened `x{helper.money(open)}` {data['items'][id]['emote']} {data['items'][id]['name']} and won a total of :dollar: `${helper.money(increase)}`",
                                       footer=" "))
            elif id == "bag":
                increase = 0
                for x in range(open):
                    increase += random.choice(data['items'][id]['extra']['winnings'])

                user.remove_inventory(id, open)
                user.add_money(increase)

                return await message.reply(
                    embed=helper.embed(message, f"{data['items'][id]['name']} Opened",
                                       f"You have opened `x{helper.money(open)}` {data['items'][id]['emote']} {data['items'][id]['name']} and got a total of :dollar: `${helper.money(increase)}`",
                                       footer=" "))
        elif data["items"][id]["item_type"] == "lootbox":
            open = 1
            amount = user.get_total_inventory(id)
            if data["items"][id]["extra"]["open_multiple"]:
                if amount > 1:
                    await message.reply(embed=helper.embed(message, "",
                                                           f"How many **{data['items'][id]['name']}** do you want to open? You currently have `{amount}` unused {data['items'][id]['name']}.",
                                                           footer=" "))

                    try:
                        msg = await client.wait_for('message', check=check, timeout=30)

                        ans = helper.clean_message(msg.content).lower()
                        ans = ans.strip()

                        if str(ans).isdigit():
                            ans = int(ans)
                            if ans > amount:
                                open = amount
                            else:
                                open = ans

                    except asyncio.TimeoutError:
                        return await message.reply(
                            embed=helper.embed(message, "Learn how to respond next time.", "", footer=" "))

            if open < 1:
                open = amount

            opened = {}
            body = ""

            for x in range(open):

                ran = random.randint(1, data["items"][id]["extra"]["items"])
                drop = mini_games.random_drop(random.randint(0, data["items"][id]["extra"]["rare"]))

                for y in range(ran):
                    max_drops = int(float(data["items"][id]["extra"]["quantity"]) * float(data["items"][drop]["rarity"]) / 100.0)
                    if max_drops < 1:
                        max_drops = 1

                    much = random.randint(1, max_drops)
                    if random.randint(1, 100) > 80:
                        drop = mini_games.random_drop(random.randint(0, data["items"][id]["extra"]["rare"]))

                    if drop in list(opened.keys()):
                        opened[drop] += much
                    else:
                        opened[drop] = much

                    user.add_inventory(drop, much)

            user.remove_inventory(id, open)

            for x in opened:
                body += f"`x{opened[x]}` —  {data['items'][x]['emote']} **{data['items'][x]['name']}**\n"

            return await message.reply(
                embed=helper.embed(message, f"{data['items'][id]['name']} Opened", body))



commands.append(Command())
