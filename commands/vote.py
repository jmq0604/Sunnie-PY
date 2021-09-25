import time

from classes import base_command
from globals import *
from helper import helper

from classes.user import UserData

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "vote"
        self.cmd = ["votes", "v"]
        self.args = False
        self.help = ""
        self.category = "Other"
        self.description = "Provides the voting URL and rewards"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 15)

    async def run(self, client, message, clean, user=UserData()):

        topgg = user.get_vote_time("topgg")
        discordbotlist = user.get_vote_time('discordbotlist')

        top_str = '[Vote Here](https://top.gg/bot/417174198843211776/vote)'
        discord_str = '[Vote Here](https://discordbotlist.com/bots/sunnie-restaurant)'

        if not time.time() - topgg > 43200:
            top_str = "`{t} LEFT`".format(t=helper.time_remaining(int(time.time() - topgg), 43200))
        if not time.time() - discordbotlist > 43200:
            discord_str = "`{t} LEFT`".format(t=helper.time_remaining(int(time.time() - discordbotlist), 43200))

        return await message.reply(
            embed=helper.embed(message, "Vote For Sunnie Restaurant",
                               f"""
__**tog.gg**__
{top_str}
------------

__**discordbotlist**__
{discord_str}
------------

**Rewards**
`x2` - <:uncommon:863403665977376779> Uncommon Loot Box
`x2` - <:vote:865110138784186368> Vote Boost
`x2` - <:kaash:857293579469717514> Bank Note
`$10,000` - :dollar: Money 

"""))





commands.append(Command())
