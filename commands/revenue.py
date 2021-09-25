import random, asyncio, math, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "module"
        self.cmd = ["mo", "modules", "mod"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "View and add to your company's modules"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:

            modules = user.company.get_modules()
            aval_modules = list(data['company']["module"].keys())

            if len(clean) > 1 and not str(clean[1]).isdigit():
                id = str(clean[1]).lower()
                if id not in aval_modules:
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} That module **does not exist** or you have not unlocked it yet!".format(
                                               e=data["emotes"]["cross"])))

                if id in modules:
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} Your company **already owns** this module! You can upgrade it using `{p}o upgrade`".format(
                                               e=data["emotes"]["cross"], p=prefix)))

                if user.company.get_money() < data['company']['module'][id]['cost']:
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} Your company do not **have enough** money to purchase this upgrade!".format(
                                               e=data["emotes"]["cross"])))

                user.company.deduct_money(data['company']['module'][id]['cost'])
                user.company.add_modules(id, data['company']['module'][id]['revenue'], data['company']['module'][id]['capacity'])

                return await message.reply(
                    embed=helper.embed(message, "",
                                       f"**{user.company.get_name()}** now has a {data['company']['module'][id]['emote']} **{data['company']['module'][id]['name']}**, enjoy the extra income!"))

            else:
                start_item = 0
                page = 1
                if len(clean) > 0 and str(clean[0]).isdigit():
                    page = (int(clean[0]) - 1)
                    if page > 0:
                        start_item = int(config.items_per_page * (int(clean[0]) - 1))
                    page += 1

                embeds = {}
                item_displayed = 0

                total_pages = math.ceil(float(len(aval_modules)) / float(config.items_per_page))
                if total_pages == 0:
                    total_pages += 1

                for x in aval_modules:
                    if x in modules:
                        title = f"{data['company']['module'][x]['emote']} {data['company']['module'][x]['name']}"
                        body = f"Revenue: `${helper.money(data['company']['module'][x]['revenue'])}/hr`\nCapacity: `{helper.money(user.company.get_modules_capacity(x))}`\nID: `{x}`\n‎‎‏‏‎ ‎‏‏‎ "
                    else:
                        title = f"{data['company']['module'][x]['emote']} {data['company']['module'][x]['name']} :lock:"
                        body = f"Cost: `${helper.money(data['company']['module'][x]['cost'])}`\nID: `{x}`\n‎‎‏‏‎ ‎‏‏‎ "

                    if start_item == 0:
                        embeds[title] = body
                        item_displayed += 1
                    else:
                        start_item -= 1

                    if item_displayed == config.items_per_page:
                        break

                if len(list(embeds.keys())) > 0:
                    embeds[list(embeds.keys())[
                        -1]] += "━━━━━━━━━━━━━━\nUse `{p}o modules [module id]` to **purchase** an module!\nUse `{p}o modules [page]` to **view** different modules!" \
                        .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

                embed = helper.embed(message, f":tools: Company Modules | Page {page}/{total_pages}",
                                     "Allows you to add modules to your company earning you extra revenue, upgrades and bonus work money",
                                     embeds=embeds)
                await message.reply(embed=embed)

        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
