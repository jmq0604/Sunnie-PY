import asyncio
import random

from classes import base_command
from classes.user import UserData

from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "work"
        self.cmd = ["w"]
        self.args = False
        self.help = ""
        self.cooldown = 600
        self.category = "Basic"
        self.description = "Play a game to earn some money by working in your pizzeria"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        pizzas = user.get_pizza()
        pizza = random.choice(pizzas)
        allowed_ingredients = list(data["pizza"]["types"][pizza]["ingredients"])
        all_ingredients = []

        total_sales = random.randint(int(user.get_capacity() / 2), user.get_capacity())
        total_profit = total_sales * (data["pizza"]["types"][pizza]["price"] + user.get_booster_type_total("work"))

        optional = []
        for x in data["pizza"]["ingredients"]:
            all_ingredients.append(x)
            if data["pizza"]["ingredients"][x]["type"] == "optional":
                optional.append(x)

        optional = random.choice(optional)
        allowed_ingredients.append(optional)

        orders = ""
        modules_done = []
        for x in user.get_modules():
            if x == "pizza" and x not in modules_done:
                orders += "During your shift, you are **tasked** to cook the following in **{ss} seconds**. Please type the __**exact recipe ( id )**__ of the following in one message:\n\n__**Pizza Orders:**__\n`x{c}` —  {e} **{n}**\n\n__Requests:__\n".format(ss=20 + user.get_total_upgrade("worktime"), ra=random.choice(data["pizza"]["comments"]), c=total_sales, n=data["pizza"]["types"][pizza]["name"], e=data["pizza"]["types"][pizza]["emote"])
                orders += str(random.choice(data["pizza"]["comments"]) + "\n").format(re=random.choice(data["pizza"]["extra_comments"]), o=data["pizza"]["ingredients"][optional]["name"])
                modules_done.append(x)

        orders += "\n\n━━━━━━━━━━━━━━\n:fork_knife_plate: **Items:** `{t}`\n:dollar: **Potential Earnings:** `${m} + bonus`".format(m=helper.money(total_profit), t=helper.money(total_sales))

        if user.settings.get_interaction():

            embed = helper.embed(message, "Order List", orders)
            await message.reply(embed=embed)

            def check(m):
                if m.author.id == message.author.id:
                    return True
                return False

            try:
                msg = await client.wait_for('message', check=check, timeout=20 + user.get_total_upgrade("worktime"))

                ans = helper.clean_message(msg.content).lower()
                split = ans.split(' ')

                correct = 0
                wrong = 0
                max_correct = len(allowed_ingredients)

                all_ingredients = [i for i in all_ingredients if i not in allowed_ingredients]
                temp = list(allowed_ingredients)

                for x in range(len(split)):
                    for y in range(len(temp)):
                        if split[x].lower() == temp[y]:
                            correct += 1
                            temp.pop(y)
                            break
                        elif split[x].lower() in all_ingredients:
                            wrong += 1
                            break

                earnt = correct - wrong
                if earnt > 0:
                    earnt = earnt / max_correct
                else:
                    earnt = 0

                total_profit = int(earnt * total_profit)
                total_sales = int(earnt * total_sales)

                user_ingredients = []

                for x in allowed_ingredients:
                    if not data["pizza"]["ingredients"][x]["type"] == "optional":
                        user_ingredients.append(user.get_total_ingredient(x))

                if min(user_ingredients) < total_sales:
                    total_profit *= min(user_ingredients) / total_sales
                    total_sales = min(user_ingredients)

                for x in allowed_ingredients:
                    if not data["pizza"]["ingredients"][x]["type"] == "optional":
                        user.remove_ingredient(x, total_sales)
                    else:
                        if user.get_total_ingredient(x) < total_sales:
                            total_profit *= 1 + (user.get_total_ingredient(x) / total_sales)
                            user.remove_ingredient(x, user.get_total_ingredient(x))
                        else:
                            total_profit *= 2
                            user.remove_ingredient(x, total_sales)

                title = "{e} Work Completed!"
                body = random.choice(data["commands"]["comment"]["great_work"])

                percentage = (correct - wrong) / max_correct * 100

                user.add_exp(random.randint(1, 50))
                if total_sales == 0:
                    body = "You sold **NONE** since you did not have any ingredients to make the pizzas. \n\n━━━━━━━━━━━━━━\nUse `{p}ingredients` to buy the things you need!\nUse `{p}recipes` to check what you need for the pizza you have unlocked!"
                else:
                    if percentage < 30:
                        body = random.choice(data["commands"]["comment"]["bad_work"])
                    elif percentage > 70:
                        body = "Great Job, you **deserve a bonus**! Here is what you **sold** from all of your modules and bonuses!\n\n__**Sold Items**__\n"

                        for x in user.get_modules():
                            if x == "pizza":

                                body += f"`x{total_sales}` —  {data['pizza']['types'][pizza]['emote']} **{data['pizza']['types'][pizza]['name']}**\n"

                                for y in pizzas:
                                    if not y == pizza:
                                        if random.randint(1, 100) < 30:

                                            sales = random.randint(int(user.get_capacity() / 2), user.get_capacity())

                                            body += f"`x{sales}` —  {data['pizza']['types'][y]['emote']} **{data['pizza']['types'][y]['name']}**\n"
                                            total_profit += sales * data['pizza']['types'][y]['price']
                                            total_sales += sales
                            else:
                                items = list(data['modules'][x]['item'])
                                random.shuffle(items)
                                items = items[0:5]

                                for y in items:
                                    if random.randint(1, 100) < 30:
                                        sales = random.randint(int(user.get_modules_capacity(x) / 2), user.get_modules_capacity(x))

                                        body += f"`x{sales}` —  {data['modules'][x]['item'][y]['emote']} **{data['modules'][x]['item'][y]['name']}**\n"
                                        total_profit += sales * data['modules'][x]['item'][y]['price']
                                        total_sales += sales


                        body += "\n\n━━━━━━━━━━━━━━\n:fork_knife_plate: **Items:** `{t}`\n:dollar: **Earnings:** `${m}`".format(
                            m=helper.money(total_profit), t=helper.money(total_sales))


                user.add_money(total_profit)
                user.add_total_sold(total_sales)
                user.statistics.add_work(1)

                return await msg.reply(embed=helper.embed(message, title.format(e=random.choice(data["commands"]["emotes"]["work"])), body.format(p=prefix, c=helper.money(total_profit), t=helper.money(total_sales)), footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))
            except asyncio.TimeoutError:
                return await message.reply(
                    embed=helper.embed(message, ":x: Work Incomplete", "You ran out of time! Better luck next time, your customers left. Use `{p}recipe` to view the recipes next time!".format(p=prefix)))
        else:
            user_ingredients = []
            for x in allowed_ingredients:
                if not data["pizza"]["ingredients"][x]["type"] == "optional":
                    user_ingredients.append(user.get_total_ingredient(x))

            if min(user_ingredients) < total_sales:
                total_profit *= min(user_ingredients) / total_sales
                total_sales = min(user_ingredients)

            for x in allowed_ingredients:
                if not data["pizza"]["ingredients"][x]["type"] == "optional":
                    user.remove_ingredient(x, total_sales)

            if total_sales == 0:
                return await message.reply(
                    embed=helper.embed(message, "{e} Work In-Completed!".format(
                        e=random.choice(data["commands"]["emotes"]["work"])),
                                       "You sold **NONE** since you did not have any ingredients to make the pizzas. \n\n━━━━━━━━━━━━━━\nUse `{p}ingredients` to buy the things you need!".format(p=prefix, c=helper.money(total_profit), t=helper.money(total_sales)),
                                       footer="Storage: {s}/{ms}".format(s=user.get_storage(),
                                                                         ms=user.get_max_storage())))

            body = "Great Job, you **deserve a bonus**! Here is what you **sold** from all of your modules and bonuses!\n\n__**Sold Items**__\n"
            for x in user.get_modules():
                if x == "pizza":

                    body += f"`x{total_sales}` —  {data['pizza']['types'][pizza]['emote']} **{data['pizza']['types'][pizza]['name']}**\n"

                    for y in pizzas:
                        if not y == pizza:
                            if random.randint(1, 100) < 30:
                                sales = random.randint(int(user.get_capacity() / 2), user.get_capacity())

                                body += f"`x{sales}` —  {data['pizza']['types'][y]['emote']} **{data['pizza']['types'][y]['name']}**\n"
                                total_profit += sales * data['pizza']['types'][y]['price']
                                total_sales += sales
                else:
                    items = list(data['modules'][x]['item'])
                    random.shuffle(items)
                    items = items[0:5]

                    for y in items:
                        if random.randint(1, 100) < 30:
                            sales = random.randint(int(user.get_modules_capacity(x) / 2), user.get_modules_capacity(x))

                            body += f"`x{sales}` —  {data['modules'][x]['item'][y]['emote']} **{data['modules'][x]['item'][y]['name']}**\n"
                            total_profit += sales * data['modules'][x]['item'][y]['price']
                            total_sales += sales

            body += "\n\n━━━━━━━━━━━━━━\n:fork_knife_plate: **Items:** `{t}`\n:dollar: **Earnings:** `${m}`".format(
                m=helper.money(total_profit), t=helper.money(total_sales))

            user.add_exp(random.randint(1, 10))
            user.add_money(total_profit)
            user.add_total_sold(total_sales)
            user.statistics.add_work(1)

            return await message.reply(
                embed=helper.embed(message, "{e} Work Completed!".format(e=random.choice(data["commands"]["emotes"]["work"])),
                                   body.format(p=prefix, c=helper.money(total_profit), t=helper.money(total_sales)),
                                   footer="Storage: {s}/{ms}".format(s=user.get_storage(), ms=user.get_max_storage())))


commands.append(Command())
