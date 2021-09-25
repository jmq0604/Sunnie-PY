import random, asyncio, math, config

from classes.server import ServerData
from classes.user import UserData
from classes.company import CompanyData

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "upgrade"
        self.cmd = ["enhance", "up", "upgrades"]
        self.args = False
        self.help = ""
        self.category = "Company"
        self.description = "View and upgrade your company"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 2, True)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        role = user.get_company_role()
        if role <= 2:

            if len(clean) > 1 and not str(clean[1]).isdigit():
                upgrades = user.company.get_available_upgrades()
                id = str(clean[1]).lower()

                if id not in upgrades:
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} That upgrade does not exist or you have not unlocked it yet!".format(
                                               e=data["emotes"]["cross"])))

                if user.company.get_money() < user.company.get_upgrade_price(id):
                    return await message.reply(
                        embed=helper.embed(message, "",
                                           "{e} Your company does not have enough money to purchase this upgrade!".format(
                                               e=data["emotes"]["cross"])))

                effects = user.company.get_upgrade_effect(id, True)
                user.company.add_upgrade(id)
                user.company.deduct_money(user.company.get_upgrade_price(id))

                body = "Your company just upgraded their **{u}**!".format(u=data['company']["upgrade"][id]["name"])
                if id == "hq":
                    print(effects)
                    user.company.add_max_cap(effects)
                    body = f"**{user.company.get_name()}** can now accept up to **{user.company.get_max_cap()}** members!"
                elif id == "exclusive":
                    user.company.add_capacity(effects)
                    body = f"**{user.company.get_name()}** can now hold up to **{user.company.get_capacity()}** customers"

                user.company.add_exp(random.randint(1, 250))
                return await message.reply(
                    embed=helper.embed(message, "{e} Purchased!".format(e=data["emotes"]["tick"]), body))
            else:
                start_item = 0
                page = 1
                if len(clean) > 1 and str(clean[1]).isdigit():
                    page = (int(clean[1]) - 1)
                    if page > 0:
                        start_item = int(config.items_per_page * (int(clean[0]) - 1))
                    page += 1

                embeds = {}
                item_displayed = 0

                upgrades = user.company.get_available_upgrades()
                total_pages = math.ceil(float(len(upgrades)) / float(config.items_per_page))
                if total_pages == 0:
                    total_pages += 1

                company_data = data["company"]["upgrade"]
                for x in upgrades:
                    if start_item == 0:
                        embeds["{e} {n} - {s}".format(s=user.company.get_total_upgrade(x), e=company_data[x]["emote"],
                                                      n=company_data[x][
                                                          "name"])] = "Info: `{i}`\nPrice: `${p}`\nEffects: `{em}{e}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏‎ " \
                            .format(i=company_data[x]["info"], id=x, p=helper.money(user.company.get_upgrade_price(x)),
                                    e=company_data[x]["format"],
                                        em=helper.money(user.company.get_upgrade_effect(x, True)))
                        item_displayed += 1
                    else:
                        start_item -= 1

                    if item_displayed == config.items_per_page:
                        break

                if len(list(embeds.keys())) > 0:
                    embeds[list(embeds.keys())[
                        -1]] += "━━━━━━━━━━━━━━\n{e} **Company Balance:** ${b}\nUse `{p}o upgrade [upgrade id]` to **purchase** an upgrade!\nUse `{p}o upgrade [page]` to **view** different pages!" \
                        .format(e=data["emotes"]["revenue"], b=helper.money(user.company.get_money()), p=prefix)

                embed = helper.embed(message,
                                     "{e} Company Upgrades | Page {page}/{total_pages}".format(total_pages=total_pages,
                                                                                           page=page,
                                                                                           e=data["emotes"]["star"]),
                                     "",
                                     embeds=embeds)

                await message.reply(embed=embed)
        else:
            return await message.reply(
                embed=helper.embed(message, f"{data['emotes']['company']} Company",
                                   f"You **do not have the rights** to use this command!"))


commands.append(Command())
