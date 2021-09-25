from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "unassign"
        self.cmd = ["ua"]
        self.args = True
        self.help = "[employee id]"
        self.category = "Employees"
        self.description = "Unassigns an employee of your choice from their job"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        user_emp = user.get_employee()
        id = str(clean[0]).lower()

        if id not in user_emp:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} You do not have any employee with that ID!!".format(
                                                              e=data["emotes"]["cross"])))

        if user.get_emp_role(id) == "none":
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} That employee is currently not working! Please use `{p}assign <employee id>` to assign them to a job!".format(
                                                              e=data["emotes"]["cross"], p=prefix)))


        role =  user.get_emp_role(id)
        revenue = user.get_emp_income(id)
        revenue_pizza = data["employee"][role]["pizza_increase"]

        user.set_emp_role(id, "none")
        user.set_emp_revenue(id, 0)
        user.deduct_revenue(revenue)
        user.deduct_revenue_pizza(revenue_pizza)

        return await message.reply(embed=helper.embed(message, "{e} Job Unassigned".format(e=data["emotes"]["tick"]),
                                                      "You have unassigned employee `{id}`!".format(id=id, role=role)))



commands.append(Command())
