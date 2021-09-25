import asyncio
import glob
import importlib
import random
import re

from os.path import dirname, basename, isfile, join

import topgg
import discord
from aiohttp import web
from discord.ext import tasks

import tasks
from classes.user import *
from classes.base_command import BaseCMD
from globals import *
from helper.sql_tables import *
from others import random_events

modules = glob.glob(join(dirname("commands/"), "*.py"))
for f in modules:
    if isfile(f):
        module = "commands." + basename(f)[:-3]
        importlib.import_module(module)


intents = discord.Intents.default()
intents.members = True


class SunnieIndustry(discord.Client):
    def __init__(self, **options):
        super().__init__(**options, intents=intents)

        self.topggpy = topgg.DBLClient(self, config.topgg, autopost=True, post_shard_count=True)
        self.topgg_webhook = topgg.WebhookManager(self).dbl_webhook("/dblwebhook", config.topgg_pass)
        self.topgg_webhook.run(8000)

    async def on_ready(self):

        asyncio.create_task(tasks.hourly_income())
        asyncio.create_task(tasks.hourly_employee())
        asyncio.create_task(tasks.daily_bank())
        asyncio.create_task(tasks.database_updates())
        asyncio.create_task(tasks.hourly_company_income())
        asyncio.create_task(tasks.reload_tasks())

        helper.webhook("start-logs", f"Booting Up - Logged in as {client.user.name}")

        for cmd in commands:
            commands_dict[cmd.name] = cmd

        print("----------------------")
        print(f'Logged in as {client.user.name}')

        TotalMembers = 0
        for x in range(len(client.guilds)):
            print(
                f'Server: {client.guilds[x].name} (id: {client.guilds[x].id}). This guild has {client.guilds[x].member_count} members!')
            TotalMembers += client.guilds[x].member_count

        print(f"\nTotal Members: {helper.money(TotalMembers)}")
        print(f"Total Servers: {len(client.guilds)}\n")
        print("----------------------\n")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=f"{config.prefix}help | https://discord.gg/xxxxxxx"))

    async def on_message(self, message):
        if message.channel.type is discord.ChannelType.private or message.author.bot:
            return

        server = ServerData(message.guild.id)
        if message.content and message.content[:len(server.get_prefix())] == server.get_prefix():

            message.content = re.sub(' +', ' ', message.content)
            split = message.content[len(server.get_prefix()):].split(' ')
            msg = split[0].lower()

            use_cmd = BaseCMD()
            for cmd in commands:
                if cmd.child:
                    continue

                if "use" in cmd.cmd:
                    use_cmd = cmd

                if msg in cmd.cmd:

                    exist = db.Exist("users", "id", str(message.author.id))
                    if not exist and not cmd.name in config.whitelisted_cmd:
                        return await message.reply(
                            embed=helper.embed(message, ":book: Whoa! First things first, you gotta setup your Shop!",
                                               "Run `{p}startup` to create your shop!".format(
                                                   p=server.get_prefix())))

                    clean = split[1:]
                    if cmd.args and not len(clean):
                        return await message.reply(embed=helper.embed(message,
                                                                      "{e} Please use the correct format!".format(e=random.choice(data["commands"]["emotes"]["format"])),random.choice(data["commands"]["comment"]["format"]).format(e=random.choice(data["commands"]["emotes"]["format"]),p=server.get_prefix(), help=str(cmd.help).format(p=server.get_prefix()))))

                    if str(f"{message.author.id}_{cmd.name}") in user_cooldown and message.author.id not in config.no_cooldown:

                        time_difference = time.time() - user_cooldown[str(f"{message.author.id}_{cmd.name}")]["time"]
                        if time_difference < cmd.cooldown:
                            return await message.reply(embed=helper.embed(message, "{e} Whao Whao!".format(
                                e=random.choice(data["commands"]["emotes"]["cooldown"])), random.choice(
                                data["commands"]["comment"]["cooldown"]).format(
                                e=random.choice(data["commands"]["emotes"]["cooldown"]), p=server.get_prefix(),
                                cmd=cmd.name, t=helper.time_remaining(time_difference, cmd.cooldown))))

                    user_cooldown[str(f"{message.author.id}_{cmd.name}")] = {"time": time.time(), "cmd": cmd.name}
                    await cmd.prerun(client, message, clean, UserData(message.author.id, message.channel.id))
                    return await random_events.start_event(client, message)

            items = list(data['items'])
            if msg.strip() in items:
                clean_message = helper.clean_message(message.content).split(" ")
                clean_message = [i for i in clean_message if i]
                return await use_cmd.run(client, message, clean_message, UserData(message.author.id, message.channel.id))

    async def on_guild_join(self, guild):
        helper.webhook("guild-logs", f"Server Joined: {guild.name} (id: {guild.id}). This guild has {guild.member_count} members!")

    async def on_guild_remove(self, guild):
        helper.webhook("guild-logs", f"Removed From: {guild.name} (id: {guild.id}). This guild has {guild.member_count} members!")

    async def on_autopost_success(self):
        helper.webhook("error-logs", f"Posted server count ({client.topggpy.guild_count}), shard count ({client.shard_count})")

    async def on_dbl_vote(self, data):

        if 'user' in data:
            site = "topgg"
            user_id = data['user']
        elif 'id' in data:
            site = "discordbotlist"
            user_id = data['id']
        else:
            return

        if "type" in data and data["type"] == "test" and int(user_id) not in config.admins:
            return

        if db.Exist("users", "id", str(user_id)):
            user = UserData(user_id)

            default_win = 1
            if 'isWeekend' in data and data['isWeekend']:
                default_win *= 2

            user.voted(site, default_win)

            try:
                user = await client.fetch_user(user.get_id())
                embedVar = discord.Embed(title="Vote Rewards", description=f"You have claimed your :dollar: **${helper.money(5000 * default_win)}** reward!\n\n__**You have Claimed the following:**__\n`x{default_win}` —  {globals.data['items']['uncommon']['emote']} **{globals.data['items']['uncommon']['name']}**\n`x{default_win}` —  {globals.data['items']['vote']['emote']} **{globals.data['items']['vote']['name']}**\n`x{default_win}` —  {globals.data['items']['banknote']['emote']} **{globals.data['items']['banknote']['name']}**\n\n", color=0x336EFF)
                await user.send(embed=embedVar)
            except Exception as e:
                helper.webhook("error-logs", f"{e}")

        helper.webhook("error-logs", f"Received a vote by {user_id}!")


client = SunnieIndustry()
client.run(config.token)
