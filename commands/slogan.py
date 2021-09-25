from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "slogan"
        self.cmd = ["motto"]
        self.args = True
        self.help = "[new name]"
        self.category = "Basic"
        self.description = "Changes your slogan for your pizzeria"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 15)

    async def run(self, client, message, clean, user):

        clean = str(" ".join(clean)).rstrip()
        clean = helper.clean_message(clean)
        
        if not str(clean).strip():
            return await message.reply(embed=helper.embed(message, "", "{e} Your slogan cannot be **empty**!".format(e=data["emotes"]["cross"], c=clean)))
        elif len(clean) > 50:
            return await message.reply(embed=helper.embed(message, "", "{e} Your slogan cannot be above **50 chracter**!".format(e=data["emotes"]["cross"], c=clean)))
        elif len(clean) < 5:
            return await message.reply(embed=helper.embed(message, "", "{e} Your slogan cannot be less than  **5 chracter**!".format(e=data["emotes"]["cross"], c=clean)))

        user.set_slogan(clean)
        await message.reply(embed=helper.embed(message, "", "{e} Your new slogan has been changed to **{c}**!".format(e=data["emotes"]["tick"], c=clean)))


commands.append(Command())
