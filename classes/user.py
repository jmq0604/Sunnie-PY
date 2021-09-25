import math, random, time, config

from helper import helper
from globals import *

from classes.server import ServerData
from classes.statistic import Statistics
from classes.company import CompanyData
from classes.settings import SettingsData

class UserData:
    def __init__(self, user_id=None, server_id=None):
        self.__userid = str(user_id).strip()
        self.statistics = Statistics(self.__userid)
        self.settings = SettingsData(self.__userid)

        if server_id:
            self.__server_id = str(server_id)
            self.server = ServerData(self.__server_id)

        exist = db.Exist("users", "id", self.__userid)
        if exist:
            db.Retrieve("users", "id", self.__userid)

            self.add_exp(random.randint(1, 5))
            self.add_bank_experience(1)

            if self.get_exp() > self.get_required_exp():
                self.add_level(1)

        if self.has_company():
            tag = str(db.Execute("SELECT tag FROM com_roles WHERE id={id}".format(id=self.__userid))[0][0])
            self.company = CompanyData(tag)

    def get_id(self):
        return self.__userid

    def get_prefix(self):
        return self.server.get_prefix()

    def self_delete(self):
        tables = db.GetAllTables()
        for x in tables:
            try:
                db.Execute(f"""DELETE FROM {x} WHERE id='{self.get_id()}';""")
            except:
                pass

    def voted(self, vote_site, amount=2):

        self.add_inventory('uncommon', amount)
        self.add_inventory('vote', amount)
        self.add_inventory('banknote', amount)
        self.add_money(5000 * amount)
        self.statistics.add_votes(1)

        r = db.Execute(f"""SELECT * FROM votes WHERE id = '{self.__userid}' AND vote_site='{vote_site}'""")
        if not r:
            db.Execute(f"INSERT INTO votes(id, vote_site) VALUES('{self.__userid}', '{vote_site}')")

        return db.Execute(f"""UPDATE votes SET timestamp = '{str(round(time.time()))}' WHERE id = '{self.__userid}' AND vote_site='{vote_site}';""")

    def get_vote_time(self, vote_site):
        try:
            return int(db.Execute(f"SELECT timestamp FROM votes WHERE id={self.__userid} AND vote_site='{vote_site}';")[0][0])
        except:
            return 0

    def get_modules(self):
        r = []
        list = db.Execute("SELECT module_id FROM modules WHERE id={id}".format(id=self.__userid))
        for x in list:
            r.append(x[0])

        return r

    def add_modules(self, module_id, income=0, capacity=0):

        list = db.Execute("SELECT module_id FROM modules WHERE id={id} AND module_id='{module_id}'".format(id=self.__userid,
                                                                                                      module_id=module_id))
        if list:
            return

        return db.Execute(f"INSERT INTO modules(id, module_id, income, capacity) VALUES('{self.__userid}', '{module_id}', '{income}', '{capacity}')")

    def get_modules_income(self, module_id):
        try:
            value = db.Execute(
                f"SELECT income FROM modules WHERE module_id='{module_id}' AND id='{self.__userid}'")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def add_modules_income(self, module_id, value=1):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(f"UPDATE modules SET income = income + '{value}' WHERE id = '{self.__userid}' AND module_id='{module_id}';")

    def get_modules_capacity(self, module_id):
        try:
            value = db.Execute(
                f"SELECT capacity FROM modules WHERE module_id='{module_id}' AND id='{self.__userid}'")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def add_modules_capacity(self, module_id, value=1):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(f"UPDATE modules SET capacity = capacity + '{value}' WHERE id = '{self.__userid}' AND module_id='{module_id}';")

    def get_modules_total_income(self):
        try:
            value = db.Execute(
                f"SELECT sum(income) FROM modules WHERE id='{self.__userid}'")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def get_capacity(self):
        return int(db.Execute("SELECT capacity FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_capacity(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "capacity", value, self.__userid)

    def add_capacity(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "capacity", value, self.__userid)

    def get_pizza(self):
        r = []
        list = db.Execute("SELECT pizza_id FROM pizza WHERE id={id}".format(id=self.__userid))
        for x in list:
            r.append(x[0])

        return r

    def get_total_pizza(self):
        return len(db.Execute("SELECT pizza_id FROM pizza WHERE id={id}".format(id=self.__userid)))

    def add_pizza(self, pizza_id):

        list = db.Execute("SELECT pizza_id FROM pizza WHERE id={id} AND pizza_id='{pizza_id}'".format(id=self.__userid, pizza_id=pizza_id))
        if list:
            return

        db.Execute(
            "INSERT INTO pizza(id, pizza_id) VALUES('{id}', '{pizza_id}')".format(id=self.__userid, pizza_id=pizza_id))

    def get_total_ingredient(self, ingredients_id):
        r = db.Execute("""SELECT * FROM ingredients WHERE id = '{id}' AND ingredients_id='{ingredients_id}'""".format(
            id=self.__userid, ingredients_id=ingredients_id))
        if not r:
            db.Execute("INSERT INTO ingredients(id, ingredients_id) VALUES('{id}', '{ingredients_id}')".format(
                id=self.__userid, ingredients_id=ingredients_id))

        return int(db.Execute(
            "SELECT amount FROM ingredients WHERE id={id} AND ingredients_id='{ingredients_id}'".format(
                id=self.__userid, ingredients_id=ingredients_id))[0][0])

    def get_ingredient(self):
        r = []
        list = db.Execute("SELECT ingredients_id FROM ingredients WHERE id={id}".format(id=self.__userid))
        for x in list:
            if self.get_total_ingredient(x[0]) > 0:
                r.append(x[0])

        return r

    def add_ingredient(self, ingredients_id, value=1):
        r = db.Execute("""SELECT * FROM ingredients WHERE id = '{id}' AND ingredients_id='{ingredients_id}'""".format(
            id=self.__userid, ingredients_id=ingredients_id))
        if not r:
            db.Execute("INSERT INTO ingredients(id, ingredients_id) VALUES('{id}', '{ingredients_id}')".format(
                id=self.__userid, ingredients_id=ingredients_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE ingredients SET amount = amount + '{value}' WHERE id = '{id}' AND ingredients_id='{ingredients_id}';""".format(
                id=self.__userid, value=value, ingredients_id=ingredients_id))

    def remove_ingredient(self, ingredients_id, value=1):
        r = db.Execute("""SELECT * FROM ingredients WHERE id = '{id}' AND ingredients_id='{ingredients_id}'""".format(
            id=self.__userid, ingredients_id=ingredients_id))
        if not r:
            db.Execute("INSERT INTO ingredients(id, ingredients_id) VALUES('{id}', '{ingredients_id}')".format(
                id=self.__userid, value=value, ingredients_id=ingredients_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE ingredients SET amount = amount - '{value}' WHERE id = '{id}' AND ingredients_id='{ingredients_id}';""".format(
                id=self.__userid, value=value, ingredients_id=ingredients_id))

    def add_booster(self, item_id, durnation, type, amount):
        use_time = helper.ntime()
        end_time = int(time.time() + durnation)

        db.Execute(
            "INSERT INTO boosters(id, item_id, use_time, end_time, type, amount) VALUES('{id}', '{item_id}', '{use_time}', '{end_time}', '{type}', '{amount}')"
            .format(id=self.__userid, item_id=item_id, use_time=use_time, end_time=end_time, type=type, amount=amount))

    def get_booster_type_total(self, type):
        try:
            value = db.Execute(
                f"SELECT sum(amount) FROM boosters WHERE type='{type}' AND id='{self.__userid}' AND CAST(strftime('%s','now') as INTEGER) < end_time")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def get_booster_active(self, item_id=None):
        if item_id:
            try:
                r = len(db.Execute(
                    """SELECT item_id FROM users INNER JOIN boosters ON boosters.id=users.id WHERE item_id='{item_id}' AND CAST(strftime('%s','now') as INTEGER) < end_time AND users.id = '{id}'""".format(
                        id=self.__userid, item_id=item_id)))

                return r
            except:
                return 0
        else:
            r = []
            list = db.Execute(
                """SELECT item_id FROM users INNER JOIN boosters ON boosters.id=users.id WHERE CAST(strftime('%s','now') as INTEGER) < end_time AND users.id = '{id}'""".format(
                    id=self.__userid))
            for x in list:
                r.append(x[0])

            return r

    def get_booster_time(self, item_id):
        r = db.Execute(
            f"SELECT end_time FROM boosters WHERE id='{self.__userid}' AND item_id='{item_id}' AND CAST(strftime('%s','now') as INTEGER) < end_time")[
            0][0]

        try:
            value = int(r)
        except:
            value = 0

        return value

    def get_storage(self):
        r = db.Execute("SELECT sum(amount) FROM ingredients WHERE id={id}".format(id=self.__userid))[0][0]

        try:
            value = int(r)
        except:
            value = 0

        return value

    def get_max_storage(self):
        r = db.Execute("SELECT max_storage FROM users WHERE id={id}".format(id=self.__userid))[0][0]

        try:
            value = int(r)
        except:
            value = 0

        return value

    def deduct_max_storage(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "max_storage", value, self.__userid)

    def add_max_storage(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "max_storage", value, self.__userid)

    def get_exp(self):
        return int(db.Execute("SELECT exp FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def get_required_exp(self):
        return config.exp_per_level * self.get_level() * self.get_level()

    def deduct_exp(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "exp", value, self.__userid)

    def add_exp(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.add_bank_experience(int(value / 3))
        db.Addition("users", "exp", value, self.__userid)

    def get_money(self):
        return int(db.Execute("SELECT cash FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_money(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.statistics.add_spent(value)
        db.Deduct("users", "cash", value, self.__userid)

    def add_money(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.statistics.add_income(value)
        db.Addition("users", "cash", value, self.__userid)

    def get_revenue(self):

        revenue = int(db.Execute("SELECT revenue FROM users WHERE id={id}".format(id=self.__userid))[0][0])
        if self.has_company():
            revenue += self.company.get_income()

        return revenue

    def deduct_revenue(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "revenue", value, self.__userid)

    def add_revenue(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "revenue", value, self.__userid)

    def get_total_sold(self):
        try:
            value = int(db.Execute("SELECT total_sold FROM users WHERE id={id}".format(id=self.__userid))[0][0])
            return value
        except:
            return 0

    def deduct_total_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "total_sold", value, self.__userid)

    def add_total_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "total_sold", value, self.__userid)

    def get_level(self):
        return int(db.Execute("SELECT level FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_level(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "level", value, self.__userid)

    def add_level(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.add_unused_skill_points(1)
        db.Addition("users", "level", value, self.__userid)

    def get_unused_skill_points(self):
        return int(db.Execute("SELECT skill_points FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_unused_skill_points(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "skill_points", value, self.__userid)

    def add_unused_skill_points(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "skill_points", value, self.__userid)

    def get_revenue_pizza(self):
        return int(db.Execute("SELECT revenue_pizza FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_revenue_pizza(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "revenue_pizza", value, self.__userid)

    def add_revenue_pizza(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("users", "revenue_pizza", value, self.__userid)

    def reset_clean(self):
        db.Update("users", "clean_time", str(round(time.time())), self.__userid)

    def get_clean(self):
        return int(db.Execute("SELECT clean_time FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def reset_daily_time(self):
        db.Update("users", "daily_time", str(round(time.time())), self.__userid)

    def get_daily_time(self):
        return int(db.Execute("SELECT daily_time FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def get_daily_amount(self):
        return int(db.Execute("SELECT daily FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def deduct_daily_amount(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("users", "daily", value, self.__userid)

    def add_daily_amount(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.statistics.add_daily(1)
        db.Addition("users", "daily", value, self.__userid)

    def set_name(self, name):

        name = helper.clean_message(name)
        db.Update("users", "shop_name", str(name), self.__userid)

    def get_name(self):
        return str(db.Execute("SELECT shop_name FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def set_slogan(self, name):

        name = helper.clean_message(name)
        db.Update("users", "slogan", str(name), self.__userid)

    def get_slogan(self):
        return str(db.Execute("SELECT slogan FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def set_location(self, name):
        db.Update("users", "location", str(name), self.__userid)

    def get_location(self):
        return str(db.Execute("SELECT location FROM users WHERE id={id}".format(id=self.__userid))[0][0])

    def get_happiness(self):
        last_clean_time = int(time.time()) - int(self.get_clean())
        if last_clean_time <= config.clean_time:
            return 100
        elif config.clean_time < last_clean_time < config.clean_grace:
            return int(100 - ((time.time() - self.get_clean() - config.clean_time) / config.clean_grace * 100))
        else:
            return 0

    def get_revenue_extra(self):

        try:
            extra = int(db.Execute("""   SELECT sum(amount) FROM users
                                            INNER JOIN boosters ON boosters.id=users.id
                                            WHERE type = 'revenue' AND CAST(strftime('%s','now') as INTEGER) < end_time AND users.id = '{id}'""".format(
                id=self.__userid))[0][0])
        except:
            extra = 0

        return extra

    def get_happiness_extra(self):

        try:
            extra = int(db.Execute("""   SELECT sum(amount) FROM users
                                INNER JOIN boosters ON boosters.id=users.id
                                WHERE type = 'percentage' AND CAST(strftime('%s','now') as INTEGER) < end_time AND users.id = '{id}'""".format(
                id=self.__userid))[0][0])
        except:
            extra = 0

        return extra

    def get_total_inventory(self, item_id):
        r = db.Execute("""SELECT * FROM user_inv WHERE id = '{id}' AND item_id='{item_id}'""".format(
            id=self.__userid, item_id=item_id))
        if not r:
            db.Execute("INSERT INTO user_inv(id, item_id) VALUES('{id}', '{item_id}')".format(
                id=self.__userid, item_id=item_id))

        return int(db.Execute("SELECT amount FROM user_inv WHERE id={id} AND item_id='{item_id}'".format(
            id=self.__userid, item_id=item_id))[0][0])

    def get_inventory(self):
        r = []
        list = db.Execute("SELECT item_id FROM user_inv WHERE id={id} AND amount > 0".format(id=self.__userid))
        for x in list:
            r.append(x[0])

        return r

    def add_inventory(self, item_id, value=1):
        r = db.Execute("""SELECT * FROM user_inv WHERE id = '{id}' AND item_id='{item_id}'""".format(
            id=self.__userid, item_id=item_id))
        if not r:
            db.Execute("INSERT INTO user_inv(id, item_id) VALUES('{id}', '{item_id}')".format(
                id=self.__userid, item_id=item_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE user_inv SET amount = amount + '{value}' WHERE id = '{id}' AND item_id='{item_id}';""".format(
                id=self.__userid, value=value, item_id=item_id))

    def remove_inventory(self, item_id, value=1):
        r = db.Execute("""SELECT * FROM user_inv WHERE id = '{id}' AND item_id='{item_id}'""".format(
            id=self.__userid, item_id=item_id))
        if not r:
            db.Execute("INSERT INTO user_inv(id, item_id) VALUES('{id}', '{item_id}')".format(
                id=self.__userid, value=value, item_id=item_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE user_inv SET amount = amount - '{value}' WHERE id = '{id}' AND item_id='{item_id}';""".format(
                id=self.__userid, value=value, item_id=item_id))

    def get_employee(self):
        r = []
        list = db.Execute("SELECT hire_id FROM user_employee WHERE id={id}".format(id=self.__userid))
        for x in list:
            r.append(x[0])

        return r

    def get_emp_price(self, price):
        price += price * (self.total_emp() * 0.2)
        return int(price)

    def add_emp(self, hire_id, dict):
        db.Execute(
            """INSERT INTO user_employee(id, hire_id, name, cost_hour, cooking, social, teamwork, management, marketing) VALUES('{user_id}', '{hire_id}', '{name_}', '{cost_hour}', '{cooking}', '{social}', '{teamwork}', '{management}', '{marketing}')"""
            .format(user_id=self.__userid, hire_id=hire_id, name_=dict["name"], cost_hour=dict["cost_hour"],
                    cooking=dict["cooking"], social=dict["social"], teamwork=dict["teamwork"],
                    management=dict["management"], marketing=dict["marketing"]))

    def remove_emp(self, hire_id):
        db.Execute(f"""DELETE FROM user_employee WHERE id='{self.__userid}' AND hire_id = '{hire_id}';""")

    def get_emp_type(self, role):

        list = db.Execute(
            "SELECT * FROM user_employee WHERE id='{id}' AND role='{role}'".format(id=self.__userid, role=role))
        if not list:
            list = []

        return list

    def set_emp_role(self, employee_id, role):
        db.Execute(
            """UPDATE user_employee SET role = '{role}' WHERE id = '{id}' AND hire_id = '{employee_id}';""".format(
                id=self.__userid, employee_id=employee_id, role=role))

    def get_emp_role(self, employee_id):
        return str(db.Execute(
            "SELECT role FROM user_employee WHERE id={id} AND hire_id = '{employee_id}'".format(id=self.__userid,
                                                                                                employee_id=employee_id))[
                       0][0]).lower()

    def get_emp_skills(self, employee_id, skill):
        return int(
            db.Execute(f"SELECT {skill} FROM user_employee WHERE id={self.__userid} AND hire_id = '{employee_id}'")[0][
                0])

    def get_emp_income(self, employee_id):
        return int(
            db.Execute(f"SELECT income FROM user_employee WHERE id={self.__userid} AND hire_id = '{employee_id}'")[0][
                0])

    def get_emp_cost(self, employee_id):
        return int(db.Execute(
            "SELECT cost_hour FROM user_employee WHERE id={id} AND hire_id = '{employee_id}'".format(id=self.__userid,
                                                                                                     employee_id=employee_id))[
                       0][0])

    def get_emp_name(self, employee_id):
        return str(db.Execute(
            "SELECT name FROM user_employee WHERE id={id} AND hire_id = '{employee_id}'".format(id=self.__userid,
                                                                                                employee_id=employee_id))[
                       0][0]).lower()

    def set_emp_revenue(self, employee_id, income):
        db.Execute(
            """UPDATE user_employee SET income = '{income}' WHERE id = '{id}' AND hire_id = '{employee_id}';""".format(
                id=self.__userid, employee_id=employee_id, income=income))

    def total_emp(self):
        return len(db.Execute("SELECT hire_id FROM user_employee WHERE id={id}".format(id=self.__userid)))

    def get_upgrade_price(self, upgrade_id):

        total = self.get_total_upgrade(upgrade_id)
        return int(
            data["upgrades"][upgrade_id]["cost"] * (total + 1) * data["upgrades"][upgrade_id]["multiplier"]) * math.exp(
            int((total + 1) / 4))

    def get_upgrade_effect(self, upgrade_id, upgrade=False):
        if not data["upgrades"][upgrade_id]["upscale"]:
            return int(data["upgrades"][upgrade_id]["effects"])

        total = self.get_total_upgrade(upgrade_id)
        if upgrade:
            total += 1

        return int(data["upgrades"][upgrade_id]["effects"] * total * data["upgrades"][upgrade_id][
            "multiplier"] * 0.75 * math.exp(int((total + 1) / 20)) + 1)

    def get_total_upgrade(self, upgrade_id):
        r = db.Execute("""SELECT * FROM upgrades WHERE id = '{id}' AND upgrade_id='{upgrade_id}'""".format(
            id=self.__userid, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO upgrades(id, upgrade_id) VALUES('{id}', '{upgrade_id}')".format(
                id=self.__userid, upgrade_id=upgrade_id))

        return db.Execute("SELECT amount FROM upgrades WHERE id={id} AND upgrade_id='{upgrade_id}'".format(
            id=self.__userid, upgrade_id=upgrade_id))[0][0]

    def get_upgrade(self):
        return db.Execute("SELECT upgrade_id FROM upgrades WHERE id={id}".format(id=self.__userid))

    def add_upgrade(self, upgrade_id, value=1):
        r = db.Execute("""SELECT * FROM upgrades WHERE id = '{id}' AND upgrade_id='{upgrade_id}'""".format(
            id=self.__userid, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO upgrades(id, upgrade_id) VALUES('{id}', '{upgrade_id}')".format(
                id=self.__userid, upgrade_id=upgrade_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE upgrades SET amount = amount + '{value}' WHERE id = '{id}' AND upgrade_id='{upgrade_id}';""".format(
                id=self.__userid, value=value, upgrade_id=upgrade_id))

    def remove_upgrade(self, upgrade_id, value=1):
        r = db.Execute("""SELECT * FROM upgrades WHERE id = '{id}' AND upgrade_id='{upgrade_id}'""".format(
            id=self.__userid, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO upgrades(id, upgrade_id) VALUES('{id}', '{upgrade_id}')".format(
                id=self.__userid, value=value, upgrade_id=upgrade_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE upgrades SET amount = amount - '{value}' WHERE id = '{id}' AND upgrade_id='{upgrade_id}';""".format(
                id=self.__userid, value=value, upgrade_id=upgrade_id))

    def get_available_location(self):
        locations = []
        for x in data["location"]:
            if data["location"][x]["level"] > data["location"][self.get_location()]["level"]:
                locations.append(x)

        return locations

    def get_available_ingredients(self):
        ingredients = []

        allowed_ingredients = []
        for x in self.get_pizza():
            for y in data["pizza"]["types"][x]["ingredients"]:
                allowed_ingredients.append(y)

        for x in data["pizza"]["ingredients"]:
            if x in allowed_ingredients or data["pizza"]["ingredients"][x]["type"] == "optional":
                ingredients.append(x)

        return ingredients

    def get_available_upgrade(self):
        upgrades = []

        modules = self.get_modules()
        for x in data["upgrades"]:
            if data["upgrades"][x]["module"] in modules:
                upgrades.append(x)

        return upgrades

    def get_available_shop(self):
        item = []

        for x in data["items"]:
                if data["items"][x]["in_shop"]:
                    item.append(x)

        return item
    
    def get_available_jobs(self):
        jobs = []
        
        modules = self.get_modules()
        max_jobs = data["location"][self.get_location()]["max"]
        for x in max_jobs:
            if data["employee"][x]["module"] in modules:
                jobs.append(x)

        return jobs

    def add_bank(self, bankid):
        if self.has_bank():
            db.Execute(f"DELETE FROM bank WHERE id='{self.__userid}';")

        db.Execute("INSERT INTO bank(id, bank_id) VALUES('{id}', '{bankid}')".format(
            id=self.__userid, bankid=bankid))

    def get_bank(self):
        if self.has_bank():
            return str(db.Execute("SELECT bank_id FROM bank WHERE id={id}".format(id=self.__userid))[0][0])

        return None

    def has_bank(self):
        return db.Exist("bank", "id", self.__userid)

    def get_bank_money(self):
        try:
            return int(db.Execute("SELECT amount FROM bank WHERE id={id}".format(id=self.__userid))[0][0])
        except:
            return 0

    def deduct_bank_money(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.statistics.add_deposit(value)
        db.Deduct("bank", "amount", value, self.__userid)

    def add_bank_money(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("bank", "amount", value, self.__userid)
        
    def get_claim(self):
        try:
            return int(db.Execute("SELECT claim FROM bank WHERE id={id}".format(id=self.__userid))[0][0])
        except:
            return 0

    def deduct_claim(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("bank", "claim", value, self.__userid)

    def add_claim(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        self.statistics.add_interest(value)
        db.Addition("bank", "claim", value, self.__userid)

    def get_bonus_max(self):
        try:
            return int(db.Execute("SELECT bonus_max FROM bank WHERE id={id}".format(id=self.__userid))[0][0])
        except:
            return 0

    def deduct_bonus_max(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("bank", "bonus_max", value, self.__userid)

    def add_bonus_max(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("bank", "bonus_max", value, self.__userid)

    def get_interest(self):
        base_interst = float(data["banks"][self.get_bank()]["interest"])
        base_interst += self.get_credit_score() / 3
        base_interst += self.get_bank_experience() / 1000

        if base_interst > 10:
            return 10

        return int(base_interst)

    def get_max_deposit(self):
        base_deposit = self.get_bank_experience() / 2
        base_deposit *= data["banks"][self.get_bank()]["max_multiplier"]
        base_deposit += self.get_bonus_max()

        return base_deposit

    def get_max_claim(self):
        base_deposit = self.get_bank_experience() / 2
        return int(base_deposit)

    def get_credit_score(self):
        try:
            return int(db.Execute("SELECT credit_score FROM bank WHERE id={id}".format(id=self.__userid))[0][0])
        except:
            return 0

    def deduct_credit_score(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("bank", "credit_score", value, self.__userid)

    def add_credit_score(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("bank", "credit_score", value, self.__userid)
    
    def get_bank_experience(self):
        try:
            return int(db.Execute("SELECT experience FROM bank WHERE id={id}".format(id=self.__userid))[0][0])
        except:
            return 0

    def deduct_bank_experience(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0
            
        exist = db.Exist("bank", "id", self.__userid)
        if exist:
            db.Deduct("bank", "experience", value, self.__userid)

    def add_bank_experience(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        exist = db.Exist("bank", "id", self.__userid)
        if exist:
            db.Addition("bank", "experience", value, self.__userid)

    def get_skill_points(self, skill_id):
        r = db.Execute("""SELECT * FROM skills WHERE id = '{id}' AND skill_id='{skill_id}'""".format(
            id=self.__userid, skill_id=skill_id))
        if not r:
            db.Execute("INSERT INTO skills(id, skill_id) VALUES('{id}', '{skill_id}')".format(
                id=self.__userid, skill_id=skill_id))

        return int(db.Execute("SELECT points FROM skills WHERE id={id} AND skill_id='{skill_id}'".format(skill_id=skill_id,id=self.__userid))[0][0])

    def add_skill_point(self, skill_id, value=1):
        r = db.Execute("""SELECT * FROM skills WHERE id = '{id}' AND skill_id='{skill_id}'""".format(
            id=self.__userid, skill_id=skill_id))
        if not r:
            db.Execute("INSERT INTO skills(id, skill_id) VALUES('{id}', '{skill_id}')".format(
                id=self.__userid, skill_id=skill_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE skills SET points = points + '{value}' WHERE id = '{id}' AND skill_id='{skill_id}';""".format(
                id=self.__userid, value=value, skill_id=skill_id))

    def remove_skill_point(self, skill_id, value=1):
        r = db.Execute("""SELECT * FROM skills WHERE id = '{id}' AND skill_id='{skill_id}'""".format(
            id=self.__userid, skill_id=skill_id))
        if not r:
            db.Execute("INSERT INTO skills(id, skill_id) VALUES('{id}', '{skill_id}')".format(
                id=self.__userid, value=value, skill_id=skill_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE skills SET points = points - '{value}' WHERE id = '{id}' AND skill_id='{skill_id}';""".format(
                id=self.__userid, value=value, skill_id=skill_id))

    def add_ban(self, reason="None"):
        if not db.Exist("ban_users", "id", self.__userid):
            db.Execute(f"INSERT INTO ban_users(id, reason) VALUES('{self.__userid}', '{reason}')")

    def remove_ban(self):
        if db.Exist("ban_users", "id", self.__userid):
            db.Execute(f"""DELETE FROM ban_users WHERE id='{self.__userid}';""")

    def has_company(self):
        return db.Exist("com_roles", "id", self.__userid)

    def get_company(self, company_tag=None, format=False):
        if not company_tag:
            if self.has_company():
                tag = str(db.Execute("SELECT tag FROM com_roles WHERE id={id}".format(id=self.__userid))[0][0])
                name = self.company.get_name()
                if format:
                    return f"[{tag}] {name}"

                return tag

            return "None"
        else:
            try:
                str(db.Execute("SELECT tag FROM company WHERE tag={company_tag}".format(company_tag=company_tag))[0][0])
                return True
            except:
                return False

    def get_company_role(self):
        if self.has_company():
            role = str(db.Execute("SELECT role FROM com_roles WHERE id={id}".format(id=self.__userid))[0][0])
            if role == "owner":
                return 1
            elif role == "co_owner":
                return 2
            elif role == "recruiter":
                return 3
            else:
                return 10
        else:
            return None