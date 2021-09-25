import random

from classes.server import *
from classes.user import *
from globals import *


def random_drop(dropchance=100):

    if dropchance > 100:
        dropchance = 100
    elif dropchance < 0:
        dropchance = 0

    drops = []
    for x in data["items"]:
        if data["items"][x]["droppable"]:
            if data["items"][x]["rarity"] >= dropchance:
                drops.append(x)

    return random.choice(drops)


def random_reward_2(body, end, user=UserData()):
    reward = config.tips_earnings + int(config.tips_earnings * float(user.get_upgrade_effect("tip")) / 100)
    reward = random.randint(int(reward / 2), reward)

    chance = random.randint(0, 10)
    if chance > 0:
        body += f":dollar: `${reward}`"
        user.add_money(reward)

    if chance > 6:
        exp = int(reward / 2)
        body += f", `{exp}` EXP {data['emotes']['xp']}"
        user.add_exp(exp)

    if chance > 7:
        total_sold = int(reward / 2)
        body += f", sold an extra `{total_sold}` {data['emotes']['pizza']}"
        user.add_total_sold(total_sold)

    if chance > 9:
        drop = random_drop(random.randint(1, 100))
        user.add_inventory(drop)
        body += f", and got a {data['items'][drop]['emote']} **{data['items'][drop]['name']}**"

    body += f". {end}"
    
    return body


async def random_reward(user, msg, title=None, rewardlim=None):
    chance = random.randint(1, 6)

    exp = int((user.get_exp() * 0.10) + 50)
    user.add_exp(exp)

    if chance == 1:
        drop = random_drop(random.randint(0, 100))

        user.add_inventory(drop)
        body = f"**{user.get_name()}** just **won** a {data['items'][drop]['emote']} **{data['items'][drop]['name']}**!"
    elif chance == 2:

        reward = int((user.get_money() * 0.10) + 5000)
        reward = random.randint(int(reward/2), reward)

        if rewardlim:
            reward = rewardlim

        user.add_money(reward)
        body = f"**{user.get_name()}** just **sold** a total sum of :dollar: `${helper.money(reward)}`!"
    elif chance == 3:
        reward = int((user.get_total_sold() * 0.05) + 50)
        reward = random.randint(int(reward/2), reward)

        if rewardlim:
            reward = int(rewardlim / 10) + 2

        user.add_total_sold(reward)
        body = f"**{user.get_name()}** just **sold** a total sum of `x{helper.money(reward)}` {data['emotes']['pizza']}!"
    elif chance == 4:
        reward = int((user.get_total_sold() * 0.05) + 50)
        reward = random.randint(int(reward / 2), reward)

        if rewardlim:
            reward = int(rewardlim / 10) + 2

        drop = random_drop(random.randint(0, 100))

        user.add_inventory(drop)
        user.add_total_sold(reward)
        body = f"**{user.get_name()}** just **sold** a total sum of `x{helper.money(reward)}` {data['emotes']['pizza']} and **won** a {data['items'][drop]['emote']} **{data['items'][drop]['name']}**!"
    elif chance == 5:
        reward = int((user.get_money() * 0.05) + 5000)
        reward = random.randint(int(reward/2), reward)
        drop = random_drop(random.randint(0, 100))

        if rewardlim:
            reward = rewardlim

        user.add_inventory(drop)
        user.add_money(reward)
        body = f"**{user.get_name()}** just **sold** a total sum of :dollar: `${helper.money(reward)}` and **won** a {data['items'][drop]['emote']} **{data['items'][drop]['name']}**!"
    else:
        body = f"**{user.get_name()}** tried their best, but the customers still seemed **unsatisfied**. Better luck next time!"
        if title:
            return await msg.reply(embed=helper.embed(msg, title, body))

        return False


    body += " Congrats to him, keep it up!"

    if title:
        return await msg.reply(embed=helper.embed(msg, title, body))

    return True


async def pharse(client, message, title, body, everyone=True):

    c_pharse = random.choice(data["minigame"]["phase"]["phases"])
    body += f"\n\n**Customers are waiting! Please type in the following Phrase:**\n\n`{c_pharse}`"

    await message.channel.send(embed=helper.embed(message, random.choice(data["events"]["messages"]), body))

    def check(m):

        if not db.Exist("users", "id", message.author.id):
            return False

        if everyone:
            if m.channel.id == message.channel.id and helper.clean_message(m.content).lower() == c_pharse:
                return True
        else:
            if m.author.id == message.author.id and helper.clean_message(m.content).lower() == c_pharse:
                return True

        return False

    msg = await client.wait_for('message', check=check, timeout=30)
    user = UserData(msg.author.id, msg.channel.id)

    await random_reward(user, msg, title)


async def unscramble(client, message, title, body, everyone=True):
    random.shuffle(words)

    random_three = words[:4]
    random_three_shuffled = []
    for x in range(len(random_three)):
        str_v = list(random_three[x])
        random.shuffle(str_v)
        random_three_shuffled.append(''.join(str_v))

    body += "You have to try to **unscramble any** of these words:\n\n"
    for y in range(len(random_three_shuffled)):
        body += "`{y}` ".format(y=random_three_shuffled[y])

    await message.channel.send(embed=helper.embed(message, random.choice(data["events"]["messages"]), body))

    def check(m):
        if not db.Exist("users", "id", message.author.id):
            return False

        if everyone:
            if m.channel.id == message.channel.id and helper.clean_message(m.content).lower() in random_three:
                return True
        else:
            if m.author.id == message.author.id and helper.clean_message(m.content).lower() in random_three:
                return True

        return False

    msg = await client.wait_for('message', check=check, timeout=30)
    user = UserData(msg.author.id, msg.channel.id)

    await random_reward(user, msg, title)
