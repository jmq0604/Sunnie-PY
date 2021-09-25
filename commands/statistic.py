from classes import base_command
from globals import *
from helper import helper

from classes.user import UserData

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "statistic"
        self.cmd = ["stats", "stat", "statistics"]
        self.args = False
        self.help = "[user]"
        self.category = "Basic"
        self.description = "Shows all your detailed statistic of the user"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 5)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        if len(clean) > 0:
            user_receive = helper.clean_message(clean[0])
            if not db.Exist("statistic", "id", user_receive):
                return await message.reply(
                    embed=helper.embed(message, f"Statistic Lookup",
                                       f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

            user = UserData(user_receive)

        embed = helper.embed(message, "{e} {name}'s Statistic".format(e=data["emotes"]["star"], name=user.get_name()),
                             f"""
**General**
{data['emotes']['term']} **Commands Sent:** `{helper.money(user.statistics.get_commands())}`
{data['emotes']['daily']} **Total Daily:** `{helper.money(user.statistics.get_daily())}`
{data['emotes']['vote']} **Total Votes:** `{helper.money(user.statistics.get_votes())}`

**Money**
{data['emotes']['income']} **Total Income:** `${helper.money(user.statistics.get_income())}`
{data['emotes']['spent']} **Total Spent:** `${helper.money(user.statistics.get_spent())}`

**Bank**
{data['emotes']['deposit']} **Total Deposit:** `${helper.money(user.statistics.get_deposit())}`
{data['emotes']['interest']} **Interest Earnt:** `${helper.money(user.statistics.get_interest())}`
{data['emotes']['transfer']} **Total Transferred:** `${helper.money(user.statistics.get_transferred())}`
{data['emotes']['received']} **Total Received:** `${helper.money(user.statistics.get_recevied())}`

**Activity**
{data['emotes']['work']} **Total Work:** `{helper.money(user.statistics.get_work())}`
{data['emotes']['tips']} **Total Tips:** `{helper.money(user.statistics.get_tips())}`
{data['emotes']['skills']} **Skills Commands:** `{helper.money(user.statistics.get_skills())}`

**Gambling**
{data['emotes']['gambling']} **Gambling Commands:** `{helper.money(user.statistics.get_gambling_commands())}`
{data['emotes']['income']} **Total Won:** `${helper.money(user.statistics.get_gambling_won())}`
{data['emotes']['spent']} **Total Lost:** `${helper.money(user.statistics.get_gambling_lost())}`
                            """)

        try:
            user = await client.fetch_user(user.get_id())
            embed.set_thumbnail(url=user.avatar_url)
        except:
            pass

        await message.reply(embed=embed)


commands.append(Command())
