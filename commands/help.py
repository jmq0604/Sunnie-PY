from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "help"
        self.cmd = ["command", "commands"]
        self.args = False
        self.help = "[command]"
        self.category = "Other"
        self.description = "Lists all the commands in the bot and what they do"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        if len(clean) > 0:
            command = str(clean[0]).lower()
            for cmd in commands:
                if cmd.name == command:
                    return await message.reply(embed=helper.embed(message, f"Help - {cmd.name}",
                                                                  f"**Alt CMD:** {helper.list_menu(cmd.cmd, True)}\n**Usage:** `{str(cmd.help).format(p=prefix)}`\n\n{cmd.description}"))

            return await message.reply(
                embed=helper.embed(message, "", "{e} That command **could not** be found!".format(e=data["emotes"]["cross"])))

        else:
            embeds = {}

            embeds["Tutorial"] = f"Run `{prefix}tutorial` to learn the basics or learn more about an aspect of the game!"
            for cmd in commands:
                if cmd.category != "Admin":
                    if f"{cmd.category} Commands" in embeds:
                        embeds[f"{cmd.category} Commands"] += f"`{cmd.name}`, "
                    else:
                        embeds[f"{cmd.category} Commands"] = f"`{cmd.name}`, "

            for x in embeds:
                embeds[x] += "\n‎‎‏‏‎ ‎‏‏‎ "

            embed = helper.embed(message, "All Commands", "".format(p=prefix), embeds=embeds, footer="Use `.help [command]` to view a specific command")
            await message.reply(embed=embed)


commands.append(Command())
