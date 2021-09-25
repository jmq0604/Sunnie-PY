from classes import base_command
from globals import *
from helper import helper
import config, math


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "jobs"
        self.cmd = ["j", "job"]
        self.args = False
        self.help = ""
        self.category = "Employees"
        self.description = "Shows all the available jobs that your pizzeria has"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        embeds = {}
        prefix = user.get_prefix()
        start_item = 0

        page = 1
        if len(clean) > 0 and str(clean[0]).isdigit():
            page = (int(clean[0]) - 1)
            if page > 0:
                start_item = int(config.items_per_page * (int(clean[0]) - 1))
            page += 1

        item_displayed = 0
        max_emp = user.get_available_jobs()

        total_pages = math.ceil(float(len(max_emp)) / float(config.items_per_page))
        if total_pages == 0:
            total_pages += 1

        for x in max_emp:
            if start_item == 0:
                embeds["{e} {n} ({t}/{m})".format(t=len(user.get_emp_type(x)), m=data["location"][user.get_location()]["max"][x],e=data["employee"][x]["emote"], n=data["employee"][x]["name"])] = "Potential Income: `${i}/hr`\nSkills: `{s}`\nID: `{id}`\n‎‎‏‏‎ ‎‏‏‎ ".format(id=x, s=data["employee"][x]["skills"], i=helper.money(data["employee"][x]["increase"]))
                item_displayed += 1
            else:
                start_item -= 1

            if item_displayed == config.items_per_page:
                break

        if len(list(embeds.keys())) > 0:
            embeds[list(embeds.keys())[
                -1]] += "━━━━━━━━━━━━━━\nUse `{p}hire` to **view** at available people for hires\nUse `{p}assign <id> <job id>` to **assign** your employees!\nUse `{p}employees` to **view** your employees!" \
                .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

        embed = helper.embed(message, f"Available Job Slots | Page {page}/{total_pages}", "", embeds=embeds)
        await message.reply(embed=embed)


commands.append(Command())
