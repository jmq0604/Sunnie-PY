import math

from classes import base_command
from globals import *
from helper import helper
from helper.sql_tables import *


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "employees"
        self.cmd = ["e"]
        self.args = False
        self.help = "<employee id>"
        self.category = "Employees"
        self.description = "Lists all your employees who you hired"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        user_emp = user.get_employee()
        prefix = user.get_prefix()

        stats = str(message.content).find("stats") > -1

        if len(clean) > 0 and not str(clean[0]).isdigit() and not str(message.content).find(" -stats") > -1:

            id = str(clean[0])
            employee = {}

            if id not in user_emp:
                return await message.reply(embed=helper.embed(message, "", "{e} You do not have any employee with that ID!!".format(e=data["emotes"]["cross"])))

            employee[id] = {
                "name": "{f}".format(f=user.get_emp_name(id)),
                "cost_hour": user.get_emp_cost(id),
                "cooking": user.get_emp_skills(id, "cooking"),
                "social": user.get_emp_skills(id, "social"),
                "teamwork": user.get_emp_skills(id, "teamwork"),
                "management": user.get_emp_skills(id, "management"),
                "marketing": user.get_emp_skills(id, "marketing")
            }

            return await message.reply(embed=helper.embed(message, ":running_shirt_with_sash: {n} | ID: {id}".format(n=employee[id]["name"], id=id), "Cooking: `{c}`\nSocial: `{s}`\nTeamwork: `{t}`\nManagement: `{m}`\nMarketing: `{ma}`\n\nHourly Salary: `${h}/hr`\n‎‎‏‏‎ ‎‏‏‎ ‎".format(
                h=employee[id]["cost_hour"], c=employee[id]["cooking"], s=employee[id]["social"],
                t=employee[id]["teamwork"], m=employee[id]["management"], ma=employee[id]["marketing"])))
        else:
            embeds = {}
            start_item = 0

            page = 1
            if len(clean) > 0 and str(clean[0]).isdigit():
                page = (int(clean[0]) - 1)
                if page > 0:
                    start_item = int(config.items_per_page * (int(clean[0]) - 1))
                page += 1

            total_pages = math.ceil(float(len(user_emp)) / float(config.items_per_page))
            if total_pages == 0:
                total_pages += 1

            item_displayed = 0
            for x in user_emp:
                if start_item == 0:
                    if stats:
                        embeds[":running_shirt_with_sash: {name}".format(name=user.get_emp_name(x))] = f'Role: `{user.get_emp_role(x)}`\nID: `{x}`\n\nCooking: `{user.get_emp_skills(x, "cooking")}`\nSocial: `{user.get_emp_skills(x, "social")}`\nTeamwork: `{user.get_emp_skills(x, "teamwork")}`\nManagement: `{user.get_emp_skills(x, "management")}`\nMarketing: `{user.get_emp_skills(x, "marketing")}` \n\nProfit: `${user.get_emp_income(x) - user.get_emp_cost(x)}/hr`\n‎‎‏‏‎ ‎‏‏‎ ‎'
                    else:
                        embeds[":running_shirt_with_sash: {name}".format(name=user.get_emp_name(x))] = "Role: `{r}`\nID: `{id}`\nProfit: `${p}/hr`\n‎‎‏‏‎ ‎‏‏‎ ‎".format(id=x, r=user.get_emp_role(x), p=user.get_emp_income(x) - user.get_emp_cost(x))
                    item_displayed += 1
                else:
                    start_item -= 1

                if item_displayed == config.items_per_page:
                    break

            if len(list(embeds.keys())) > 0:
                embeds[list(embeds.keys())[
                    -1]] += "━━━━━━━━━━━━━━\nUse `{p}assign [id] [job]` to assign your employees!\nUse `{p}job` to view your shop's available jobs!\nUse `{p}employees [id]` to view your employee's stats!" \
                    .format(e=data["emotes"]["revenue"], b=helper.money(user.get_money()), p=prefix)

            embed = helper.embed(message, "{name}'s Employees | Page {page}/{total_pages}".format(total_pages=total_pages, page=page, name=message.author.name), "".format(p=prefix), embeds=embeds, footer="Use `{p}e <page no>` to view other pages or `-stats` for full stats".format(p=prefix))
            await message.reply(embed=embed)


commands.append(Command())
