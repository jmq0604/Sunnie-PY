from classes import base_command
from globals import *
from helper import helper

import config, math, asyncio


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "bank"
        self.cmd = ["ba", "b"]
        self.args = False
        self.help = ""
        self.category = "Bank"
        self.description = "Lists the available banks or shows your bank account information"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 3)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        arg = " "
        if len(clean) > 0:
            arg = clean[0]

        has_bank = user.has_bank()

        if len(clean) > 0 and not str(clean[0]).isdigit():
            id = str(clean[0])
            banks = list(data['banks'])
            if id not in banks:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} That bank does not exist!".format(
                                           e=data["emotes"]["cross"]), footer=" "))

            if user.get_money() < data['banks'][id]["price"]:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} You need `${p}` to open a bank account!".format(
                                           e=data["emotes"]["cross"], p=helper.money(data['banks'][id]["price"])), footer=" "))

            if has_bank:
                def check(m):
                    if m.author.id == message.author.id:
                        return True
                    return False

                try:
                    await message.reply(embed=helper.embed(message, ":warning: Bank Change",
                                                           "Please reply with a `yes` if you like to switch banks! If you do so, all of your **progress will be reset** on your current bank!"))
                    msg = await client.wait_for('message', check=check, timeout=30)

                    ans = helper.clean_message(msg.content).lower()
                    if ans == "yes" or ans == "y":
                        can_switch = True
                    else:
                        can_switch = False

                except asyncio.TimeoutError:
                    can_switch = False
            else:
                can_switch = True

            if can_switch:

                user.deduct_money(data['banks'][id]["price"])
                user.add_bank(id)

                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} Congrats! You now have a bank account, you can now **withdraw and deposit** cash into it!".format(
                                           e=data["emotes"]["tick"])))

            else:
                return await message.reply(
                    embed=helper.embed(message, "",
                                       "{e} Your bank will not be selected or switched!".format(
                                           e=data["emotes"]["cross"])))
        elif arg == "view" or not has_bank:
            embeds = {}
            start_item = 0
            page = 1

            if len(clean) > 1 and str(clean[1]).isdigit():
                page = (int(clean[1]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[1]) - 1))
                page += 1

            item_displayed = 0
            banks = list(data['banks'])

            total_pages = math.ceil(float(len(banks)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            for x in banks:
                if start_item == 0:
                    embeds["{em} **{e}**".format(e=data["banks"][x]["name"], em=data["banks"][x]["emote"])] = "Price: `${p}`\nInterest: `{i}%/day`\nScore Rates: `x{s}`\nDeposit Rates: `x{d}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏ ‎".format(p=helper.money(data['banks'][x]["price"]), s=data["banks"][x]["score_multiplier"], d=data["banks"][x]["max_multiplier"], i=data["banks"][x]["interest"], id=x)
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\nUse `{p}bank [id]` to **choose** a bank!\nUse `{p}bank` to **view** your bank balances!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "Banks | Page {page}/{total_pages}".format(total_pages=total_pages, page=page), "", embeds=embeds, footer="Use `{p}location <page no>` to view other pages".format(p=prefix))
            await message.reply(embed=embed)
        else:
            embed = helper.embed(message,  f":bank: Bank", f"{data['banks'][user.get_bank()]['name']}",
                                 embeds={
                                     "Balances": f"<:vault:863350487201218570> `${helper.money(user.get_bank_money())}/${helper.money(user.get_max_deposit())}`",
                                     "Interest": f"<:interest:863351688303214622> `${helper.money(user.get_claim())}/${helper.money(user.get_max_claim())}`",
                                     "Rates ( daily )": f"<:rates:863352157789224990> {user.get_interest()}%",
                                     "Credit Score": f":credit_card: {user.get_credit_score()}"
                                 })

            embed.set_thumbnail(url=message.author.avatar_url)
            await message.reply(embed=embed)


commands.append(Command())
