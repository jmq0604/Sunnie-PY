import asyncio

from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "fire"
        self.cmd = ["f"]
        self.args = True
        self.help = "[employee id]"
        self.category = "Employees"
        self.description = "Fires an employee of your choice"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        user_emp = user.get_employee()
        id = str(clean[0]).lower()

        if id not in user_emp:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} You do not have any employee with that ID!!".format(
                                                              e=data["emotes"]["cross"])))

        if not user.get_emp_role(id) == "none":
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} That employee is currently working in a role! Please use `{p}unassign <employee id>` to fire them!".format(
                                                              e=data["emotes"]["cross"], p=prefix)))

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        try:

            await message.reply( embed=helper.embed(message, ":warning: Fire In-Progress", "Please reply with a `yes` if you like to fire that employee, that employee cannot be returned once fired!"))
            msg = await client.wait_for('message', check=check, timeout=30)

            ans = helper.clean_message(msg.content).lower()
            if ans == "yes" or ans == "y":

                name = user.get_emp_name(id)
                user.add_revenue(user.get_emp_cost(id))
                user.remove_emp(id)

                return await message.reply(embed=helper.embed(message, "{e} Employee Fired".format(e=data["emotes"]["tick"]), f"You have successfully fired **{name}**!"))
            else:
                return await message.reply(
                    embed=helper.embed(message, ":x: Fire Failed",
                                       "You chose to not fire him, therefore he will continue to stay in your pizzeria!"))
        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Fire Failed",
                                   "You ran out of time! Please respond next time!".format(
                                       p=prefix)))


commands.append(Command())
