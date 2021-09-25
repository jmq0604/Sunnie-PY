from classes.user import *


class BaseCMD:
    def __init__(self, cmd=None, name="none", help=None, cooldown=3, child=False):
        self.name = name
        self.cmd = cmd
        self.cooldown = cooldown
        self.child = child

        if cmd:
            self.cmd.append(self.name)

        if help:
            self.help = "{p}" + self.name + " " + help

    async def prerun(self, client, message, clean, user):
        print(f'{message.guild.name} - {message.author.name}: {message.content}')

        if db.Exist("ban_users", "id", message.author.id) or db.Exist("ban_Servers", "id", message.guild.id):
            return

        try:
            if self.category == "Admin":
                if message.author.id not in config.admins:
                    return
        except:
            pass  # to-do add filter

        await self.run(client, message, clean, user)
        await self.postrun(client, message, clean, user)

    async def postrun(self, client, message, clean, user):
        try:
            if self.category == "Gambling":
                user.statistics.add_gambling_commands(1)
        except:
            print(f"WARNING: Command {self.name} missing category attribute")
            helper.webhook("error-logs", f"WARNING: Command {self.name} missing category attribute")

        user.statistics.add_command(1)
        helper.webhook("cmd-logs", f'{message.guild.name} - {message.author.name}: {message.content}')

    async def run(self, client, message, clean, user):
        pass
