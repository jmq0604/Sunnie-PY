import asyncio
import random

from classes import base_command
from classes.user import *
from globals import *
from others import mini_games


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "search"
        self.cmd = ["find"]
        self.args = False
        self.help = ""
        self.category = "Basic"
        self.description = "Go out to the streets and start searching for items"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 60)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        places = list(data["commands"]["search"].keys())

        random.shuffle(places)
        places = places[0:3]

        await message.reply(
            embed=helper.embed(message, f"Searching",
                               f"Please **choose and type** one of the following places to search\n\n`{places[0]}` ‎‏‏‎ `{places[1]}` ‎‏‏‎ `{places[2]}`",  footer=""))

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        try:
            msg = await client.wait_for('message', check=check, timeout=20)

            ans = helper.clean_message(msg.content).lower()

            if ans not in places:
                return await message.reply(
                    embed=helper.embed(message, f":x: Search Failed",
                               f"Not sure what place that is, but its not from the list you dummy.", footer=" "))

            chance = random.randint(0, 100)
            user.add_exp(random.randint(1, 5))

            title = "Search Completed"
            if chance < 65:
                reward = random.randint(0, 250)
                drop = mini_games.random_drop(random.randint(1, 100))

                reward_str = f":dollar: `${reward}`"
                if random.randint(0,100) > 95:
                    user.add_inventory(drop)
                    reward_str += f" and a {data['items'][drop]['emote']} **{data['items'][drop]['name']}**"

                user.add_money(reward)
                body = random.choice(data["commands"]["search"][ans]["win"]).format(p=reward_str)

            elif chance < 95:
                body = random.choice(data["commands"]["search"][ans]["lost"]).format(p=f"")

            else:
                print(chance)
                title = "Killed In Action"
                lost = random.randint(0, 500)

                if user.get_money() < lost:
                    lost = user.get_money()

                user.deduct_money(lost)
                body = random.choice(data["commands"]["search"][ans]["die"]).format(p=f":dollar: `${helper.money(lost)}`")

            return await msg.reply(embed=helper.embed(message, title, body, footer=" "))

        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Search Failed", "Type a place you want to search next time you dummy".format(p=prefix),  footer=" "))



commands.append(Command())
