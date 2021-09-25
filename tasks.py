import asyncio, random, config, time, globals

from classes.company import CompanyData
from classes.user import UserData
from globals import employees, data, db
from helper import helper


async def database_updates():
    while True:
        db.Commit()
        await asyncio.sleep(10)


async def reload_tasks():
    while True:
        possible_tasks = list(data["tasks"].keys())
        random.shuffle(possible_tasks)

        globals.daily_tasks = {}

        globals.daily_tasks["tasks"] = {}
        for x in range(3):
            task = possible_tasks[x]
            globals.daily_tasks["tasks"][task] = {
                "name": data['tasks'][task]['name'],
                "value": random.choice(data['tasks'][task]['value']),
                "cash": random.randint(int(data['tasks'][task]['cash']/2), data['tasks'][task]['cash']),
                "exp": random.randint(int(data['tasks'][task]['exp']/2), data['tasks'][task]['exp'])
            }

        globals.daily_tasks['time'] = time.time()

        helper.webhook("error-logs", f"Daily task has been updated!")
        await asyncio.sleep(config.tasks_reload)


async def add_all_database(client):
    for x in range(len(client.users)):
        helper.webhook("error-logs", f"{x} {client.users[x].name}")

        user = UserData(client.users[x].id, 0)

        db.Retrieve("users", "id", str(client.users[x].id))
        db.Update("users", "clean_time", str(round(time.time())), str(client.users[x].id))

        pizza = list(data["pizza"]["types"].keys())[0]

        user.add_pizza(pizza)
        user.add_modules("pizza")


async def daily_bank():
    while True:

        user_list = db.Execute("""SELECT id FROM bank""".format(c=config.clean_grace))
        for x in user_list:
            x = x[0]

            user = UserData(x)

            current = user.get_bank_money()
            interest = user.get_interest()
            addition = current * (interest / 100.0)
            if user.get_claim() + addition > user.get_max_claim():
                addition = user.get_max_claim() - user.get_claim()

            user.add_claim(addition)
            await asyncio.sleep(0)

        helper.webhook("error-logs", "Bank & Interest has been updated for {n}!".format(n=len(user_list)))
        await asyncio.sleep(86400)


async def hourly_company_income():
    while True:

        await asyncio.sleep(3600)

        company_list = db.Execute(
            """SELECT tag FROM company WHERE CAST(strftime('%s','now') as INTEGER) < tax_return + '{c}'""".format(
                c=config.company_cooldown))

        for x in company_list:
            x = x[0]

            company = CompanyData(x)

            company.add_money(company.get_income())
            company.add_total_sold(company.get_income_sold())

            await asyncio.sleep(0)

        helper.webhook("error-logs", "Company income has been updated for {n}!".format(n=len(company_list)))


async def hourly_income():
    while True:

        await asyncio.sleep(3600)

        user_list = db.Execute(
            """SELECT id FROM users WHERE CAST(strftime('%s','now') as INTEGER) < clean_time + '{c}'""".format(
                c=config.clean_grace))
        for x in user_list:
            x = x[0]

            user = UserData(x)

            rev_income = user.get_revenue() + user.get_modules_total_income()
            rev_sales = user.get_revenue_pizza()
            percentage = user.get_happiness()

            happ_extra = user.get_happiness_extra()
            rev_income += user.get_revenue_extra() + (rev_income * happ_extra / 100)
            rev_sales += (rev_sales * happ_extra / 100)

            rev_income *= percentage / 100
            rev_sales *= percentage / 100

            user.add_money(rev_income)
            user.add_total_sold(rev_sales)

            await asyncio.sleep(0)

        helper.webhook("error-logs", "Cash and Sold has been updated for {n}!".format(n=len(user_list)))


async def hourly_employee():
    while True:
        globals.employees = {}
        for x in range(4):

            random_skills = []
            for y in range(5):
                chance = random.randint(0, 10)
                if chance < 6:
                    random_skills.append(random.randint(4, 7))
                elif chance > 8:
                    random_skills.append(random.randint(4, 8))
                else:
                    random_skills.append(random.randint(4, 10))

            globals.employees[str(helper.random_id(3))] = {
                "name": "{f} {l}".format(f=random.choice(data['others']['first_names']),
                                         l=random.choice(data['others']['last_names'])),
                "price": random.randint(3000, 5000),
                "cost_hour": random.randint(3, sum(random_skills)),
                "cooking": random_skills[0],
                "social": random_skills[1],
                "teamwork": random_skills[2],
                "management": random_skills[3],
                "marketing": random_skills[4],
                "total": sum(random_skills)
            }

        helper.webhook("error-logs", "Employees has been set!")
        await asyncio.sleep(3600)
