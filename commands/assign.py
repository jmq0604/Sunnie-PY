from classes import base_command

from classes.user import *

class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "assign"
        self.cmd = ["a"]
        self.args = True
        self.help = "[employee id] [job id]"
        self.category = "Employees"
        self.description = "Assigns an employee to one of the available job"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        if len(clean) < 2:
            return await message.reply(embed=helper.embed(message, "Please use the correct format!",
                                                   str("{e} Usage - `" + self.help + "`").format(
                                                       e=data["emotes"]["cross"], p=prefix)))

        user_emp = user.get_employee()
        id = str(clean[0]).lower()
        if id not in user_emp:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} You do not have any employee with that ID!!".format(
                                                              e=data["emotes"]["cross"])))

        if not user.get_emp_role(id) == "none":
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} That employee is currently working in another role! Please use `{p}unassign <employee id>` to remove their role!".format(
                                                              e=data["emotes"]["cross"], p=prefix)))

        role = str(clean[1]).lower()
        max_emp = user.get_available_jobs()
        if role not in max_emp:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} There is no job position with that name!".format(
                                                              e=data["emotes"]["cross"])))

        if len(user.get_emp_type(role)) >= data["location"][user.get_location()]["max"][role]:
            return await message.reply(embed=helper.embed(message, "",
                                                          "{e} You cannot hire anymore employees to that job anymore!".format(
                                                              e=data["emotes"]["cross"])))

        revenue = float(data["employee"][role]["increase"])
        revenue_pizza = float(data["employee"][role]["pizza_increase"])

        skills_needed =  data["employee"][role]["skills"]
        revenue *= float(user.get_emp_skills(id, skills_needed) / 10)
        revenue = int(revenue)

        user.set_emp_role(id, role)
        user.set_emp_revenue(id, revenue)
        user.add_revenue(revenue)
        user.add_revenue_pizza(revenue_pizza)

        return await message.reply(embed=helper.embed(message, "{e} Job Assigned".format(e=data["emotes"]["tick"]),
                                                      "You have assigned employee `{id}` to {role}! You can use `{p}unassign <employee id>` to remove their job role in the future!".format(id=id, role=role, p=prefix)))



commands.append(Command())
