import random
import re
import time

import discord
from discord_webhook import DiscordWebhook

from globals import *


def webhook(url, content):
    try:
        a_url = data["webhook"][url]
        webhook = DiscordWebhook(url=a_url, content=f"```{content}```")
        response = webhook.execute()
    except:
        print(content)


def embed(message, title, description, embeds=None, footer=None, inline=False):
    embed = discord.Embed(title=title, description=description, color=discord.Colour.random())

    if embeds:
        for x in embeds.keys():
            embed.add_field(name=x, value=embeds[x], inline=inline)

    if not footer:
        if random.randint(0, 100) > 50:
            footer = random.choice(data['others']['fun_facts'])
        else:
            footer = f"Use *help to view other commands"

    embed.set_footer(text=footer)

    return embed


def clean_message(msg):
    msg = re.sub(r'[^\w]', ' ', msg)
    msg = msg.rstrip()
    msg = re.sub(' +', ' ', msg)
    return msg


def compare_list(list1, list2):
    count = 0
    for x in range(len(list1)):
        for y in range(len(list2)):
            if list1[x] == list2[y]:
                count += 1
                break

    return count


def list_menu(list_, encodes=False):
    r = ""
    for x in range(len(list_)):
        if x == len(list_) - 1:
            if encodes:
                r += f"`{list_[x]}` "
            else:
                r += list_[x]
        else:
            if encodes:
                r += f"`{list_[x]}`, "
            else:
                r += list_[x] + ", "
    return r


def random_id(size=10):
    random_string = ''
    for _ in range(size):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string.lower()


def money(text):
    text = int(text)
    return "{:,}".format(text)


def ntime():
    return str(round(time.time()))


def time_remaining(difference, cool):
    time_left = round(int(cool) - int(difference))
    if time_left < 0:
        return "0 seconds"

    if time_left < 60:
        return str(time_left) + " seconds"
    elif time_left < 3600:
        return str(round(time_left / 60)) + " minutes"
    elif time_left < 86400:
        return str(round(time_left / 60 / 60)) + " hours"
    else:
        return str(round(time_left / 60 / 60 / 24)) + " days"


def time_human(second):
    if second < 60:
        return str(second) + " seconds"
    elif second < 3600:
        return str(round(second / 60)) + " minutes"
    elif second < 86400:
        return str(round(second / 60 / 60)) + " hours"
    elif second < 86400:
        return str(round(second / 60 / 60 / 60)) + " hours"
    else:
        return str(round(second / 60 / 60 / 60 / 24)) + " days"


def statement(st, true, false):
    if st:
        return true
    else:
        return false