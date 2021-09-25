import random, asyncio, time, config, math

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "settings"
        self.cmd = ["config", "ss", "setting"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Allows you to see and change different settings"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        args = ""
        if len(clean) > 0:
            args = clean[0]

        if args:
            settings = list(data['settings'].keys())

            if args not in settings:
                return await message.reply(
                    embed=helper.embed(message, f"",
                                       f":x: **That is not a valid setting!**", footer=' '))

            try:
                toggle = 0
                if str(clean[1]).lower() in ["on", "1", "enable"]:
                    toggle = 1

                user.settings.set_settings(args, toggle)
                return await message.reply(
                    embed=helper.embed(message, f"Settings",
                                       f"You have **successfully changed** your settings!"))

            except:
                return await message.reply(
                    embed=helper.embed(message, f"Settings",
                                       f"Please enter a valid option next time, `settings {args} [on/off]`!"))


        else:
            embeds = {}
            start_item = 0

            page = 1
            if len(clean) > 0 and str(clean[0]).isdigit():
                page = (int(clean[0]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[0]) - 1))
                page += 1

            item_displayed = 0
            all_settings = user.settings.all_settings()

            total_pages = math.ceil(float(len(all_settings)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            for x in range(len(all_settings)):
                if start_item == 0:

                    if bool(all_settings[x][1]):
                        status = "Status: `ON` :green_circle:"
                    else:
                        status = "Status: `OFF` :red_circle:"

                    embeds[f"{all_settings[x][0]}"] = f"*{data['settings'][all_settings[x][0]]}*\n{status}"
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            embed = helper.embed(message,
                                 "Settings | Page {page}/{total_pages}".format(total_pages=total_pages,
                                                                               page=page),
                                 "Welcome to your settings page, you can toggle a item by doing `{p}settings [item] [on/off]`".format(
                                     p=prefix), embeds=embeds,
                                 footer="Use `{p}settings <page no>` to view other pages".format(p=prefix))
            await message.reply(embed=embed)


commands.append(Command())
