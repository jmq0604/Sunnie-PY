from classes import base_command
from globals import *
from helper import helper

import discord, time
from classes.user import UserData

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "profile"
        self.cmd = ["p", "bal", "store"]
        self.args = False
        self.help = "[user]"
        self.category = "Basic"
        self.description = "Shows the user's profile"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 3)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        if len(clean) > 0:
            user_receive = helper.clean_message(clean[0])
            if not db.Exist("users", "id", user_receive):
                return await message.reply(
                    embed=helper.embed(message, f"Profile Lookup",
                                       f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

            user = UserData(user_receive)

        extra_income = user.get_revenue_extra()
        extra_income_str = ""
        if extra_income:
            extra_income_str = "( +${ex}/hr )".format(ex=extra_income)

        extra_happiness = user.get_happiness_extra()
        extra_happiness_str = ""
        if extra_happiness:
            extra_happiness_str = "( +{em}% )".format(em=extra_happiness)

        emotes = data['emotes']
        embed = discord.Embed(title=f":star: {user.get_name()}", description=f"*{user.get_slogan()}*")

        # LOCATION
        embed.add_field(name='Location', value="{e} {location} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ \n:busts_in_silhouette: {t} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ "
                        .format(e=data["location"][user.get_location()]["emote"], location=data["location"][user.get_location()]["name"],
                                t=helper.money(user.total_emp())), inline=True)

        # COMPANY
        if user.has_company():
            embed.add_field(name='Company', value=f"{emotes['company']} {user.get_company(format=True)} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ ", inline=True)

        # CASH
        cash_str = f"{emotes['cash']} ${helper.money(user.get_money())} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ "
        if user.has_bank():
            cash_str += f"\n{emotes['bank']} ${helper.money(user.get_bank_money())}"
        cash_str += f"\n{emotes['inv']} {helper.money(len(user.get_inventory()))} items"

        embed.add_field(name='Cash', value=cash_str, inline=True)

        # Revenue
        embed.add_field(name='Revenue/hr', value="{e} ${c} {ex} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ \n{ea} {cm} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ ".format(ex=extra_income_str, e=data["emotes"]["revenue"],
                                                     ea=data["emotes"]["pizza"], c=helper.money(user.get_revenue()),
                                                     cm=helper.money(user.get_revenue_pizza())), inline=True)


        # TOTAL SOLD
        embed.add_field(name='Total Sold',
                        value="{e} {c} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ \n:unlock: {piz} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ ".format(piz=user.get_total_pizza(), e=data["emotes"]["pizza"], c=helper.money(user.get_total_sold())), inline=True)


        # STORE
        embed.add_field(name='Store', value="{e} {h}% {ex} ‎‏‏‎  ‎‏‏‎ \n{ee} {hh} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ ".format(ex=extra_happiness_str, e=data["emotes"]["clean"], h=user.get_happiness(), ee=data["emotes"]["capacity"], hh=helper.money(user.get_capacity())), inline=True)

        # LEVELS
        embed.add_field(name='Level', value="{e} {c} - {exp}/{max} ‎‏‏‎  ‎‏‏‎  ‎‏‏‎  ‎‏‏‎ ".format(max=helper.money(user.get_required_exp()), exp=helper.money(user.get_exp()), e=data["emotes"]["level"], ee=data["emotes"]["xp"], c=helper.money(user.get_level())), inline=True)

        # MODULES
        modules_str = "‎‎"
        for x in user.get_modules():
            if x != "pizza":
                modules_str += f"{data['modules'][x]['emote']} {data['modules'][x]['name']} ━  `${helper.money(user.get_modules_income(x))}/hr` | `{helper.money(user.get_modules_capacity(x))} cap`\n ‎‏‏‎ "

        if len(modules_str) > 3:
            embed.add_field(name='Modules', value=modules_str, inline=False)

        # BOOST
        boost_str = ""
        for x in user.get_booster_active():
            boost_str += f"{data['items'][x]['emote']} **{data['items'][x]['name']}**: `{helper.time_human(user.get_booster_time(x) - time.time())}` Remaining \n"

        if len(boost_str) > 3:
            embed.add_field(name='Active Boosts', value=boost_str, inline=False)

        embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        embed.set_thumbnail(url=message.author.avatar_url)

        await message.reply(embed=embed)


commands.append(Command())
