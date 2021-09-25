from classes import base_command

from classes.user import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "modules"
        self.cmd = ["m", "module"]
        self.args = False
        self.help = "[module id]"
        self.category = "Expand"
        self.description = "Shows what 'addons' you can add to your pizzeria to generate more income"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 5)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()

        modules = user.get_modules()
        aval_modules = list(data["modules"].keys())

        if len(clean) > 0 and not str(clean[0]).isdigit():
            id = str(clean[0]).lower()
            if id not in aval_modules:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} That module **does not exist** or you have not unlocked it yet!".format(
                                           e=data["emotes"]["cross"])))

            if id in modules:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} You have **already purchased** this module! You can upgrade it using `{p}upgrade`".format(
                                           e=data["emotes"]["cross"], p=prefix)))

            if user.get_money() < data['modules'][id]['cost']:
                return await message.reply(
                    embed=helper.embed(message, "", "{e} You do not **have enough** money to purchase this upgrade!".format(
                        e=data["emotes"]["cross"])))

            user.deduct_money(data['modules'][id]['cost'])
            user.add_modules(id, data['modules'][id]['revenue'], data['modules'][id]['capacity'])

            return await message.reply(
                embed=helper.embed(message, "", "{e} You have just **purchased** the module! Enjoy the **extra** revenue **hourly** and at **work**!".format(
                    e=data["emotes"]["tick"])))

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
                    title = f"{data['modules'][x]['emote']} {data['modules'][x]['name']}"
                    body = f"Revenue: `${helper.money(data['modules'][x]['revenue'])}/hr`\nCapacity: `{helper.money(user.get_modules_capacity(x))}`\nID: `{x}`\n‎‎‏‏‎ ‎‏‏‎ "
                else:
                    title = f"{data['modules'][x]['emote']} {data['modules'][x]['name']} :lock:"
                    body = f"Cost: `${helper.money(data['modules'][x]['cost'])}`\nID: `{x}`\n‎‎‏‏‎ ‎‏‏‎ "

                if start_item == 0:
                    embeds[title] = body
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\nUse `{p}modules [module id]` to **purchase** an module!\nUse `{p}modules [page]` to **view** different modules!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, f":tools: Modules | Page {page}/{total_pages}", "Allows you to add modules to your shop earning you extra revenue, upgrades and bonus work money", embeds=embeds)
            await message.reply(embed=embed)



commands.append(Command())
