from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "name"
        self.cmd = ["rename", "title"]
        self.args = True
        self.help = "[new name]"
        self.category = "Basic"
        self.description = "Renames your pizzeria's name"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 15)

    async def run(self, client, message, clean, user):

        clean = str(" ".join(clean)).rstrip()
        clean = helper.clean_message(clean)
        
        if not str(clean).strip():
            return await message.reply(embed=helper.embed(message, "", "{e} Your name cannot be **empty**!".format(e=data["emotes"]["cross"], c=clean)))
        elif len(clean) > 20:
            return await message.reply(embed=helper.embed(message, "", "{e} Your name cannot be above **20 chracters**!".format(e=data["emotes"]["cross"], c=clean)))
        elif len(clean) < 5:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} Your name cannot be less than **5 chracters**!".format(
                                                              e=data["emotes"]["cross"], c=clean)))

        user.set_name(clean)
        await message.reply(embed=helper.embed(message, "", "{e} Your shop has been renamed to **{c}**!".format(e=data["emotes"]["tick"], c=clean),None))


commands.append(Command())
