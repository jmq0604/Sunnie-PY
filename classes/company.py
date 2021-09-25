import time, re, config, random, math

from helper import helper
from globals import *


class CompanyData:
    def __init__(self, company_tag, owner_id=None):
        self.__company_tag = str(company_tag).upper().strip()

        if not db.Exist("company", "tag", self.__company_tag):
            db.Retrieve("company", "tag",  self.__company_tag)
            db.Execute("""UPDATE company SET owner = '{owner_id}' WHERE tag = '{tag}';""".format(owner_id=str(owner_id).strip(), tag=self.__company_tag))
        else:
            self.add_exp(random.randint(1, 2))
            if self.get_exp() > self.get_required_exp():
                self.add_level(1)

    def get_tag(self):
        return self.__company_tag

    def get_owner(self):
        return str(db.Execute("SELECT owner FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def get_co_owner(self):
        try:
            return str(db.Execute("SELECT id FROM com_roles WHERE tag='{tag}' AND role='co_owner'".format(tag=self.__company_tag))[0][0])
        except:
            return None

    def get_name(self):
        return str(db.Execute("SELECT company_name FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def set_name(self, name):
        name = helper.clean_message(name)
        db.Update("company", "company_name", str(name), self.__company_tag, "tag")

    def get_motto(self):
        return str(db.Execute("SELECT motto FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def set_motto(self, motto):
        motto = helper.clean_message(motto)
        db.Update("company", "motto", str(motto), self.__company_tag, "tag")

    def get_money(self):
        return int(db.Execute("SELECT money FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def add_money(self, value=1):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE company SET money = money + '{value}' WHERE tag = '{tag}';""".format(
                tag=self.__company_tag, value=value))

    def deduct_money(self, value=1):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE company SET money = money - '{value}' WHERE tag = '{tag}';""".format(
                tag=self.__company_tag, value=value))

    def get_upgrade_price(self, upgrade_id):

        total = self.get_total_upgrade(upgrade_id)
        return int(data["company"]["upgrade"][upgrade_id]["cost"] * (total + 1) * data["company"]["upgrade"][upgrade_id]["multiplier"])

    def get_upgrade_effect(self, upgrade_id, upgrade=False):
        total = self.get_total_upgrade(upgrade_id)
        if upgrade:
            total += 1

        return int(data["company"]["upgrade"][upgrade_id]["increase"] * total * data["company"]["upgrade"][upgrade_id]["multiplier"] / 2)

    def get_total_upgrade(self, upgrade_id):
        r = db.Execute("""SELECT * FROM com_upgrade WHERE tag='{id}' AND upgrade_id='{upgrade_id}'""".format(
            id=self.__company_tag, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO com_upgrade(tag, upgrade_id) VALUES('{id}', '{upgrade_id}')".format(
                id=self.__company_tag, upgrade_id=upgrade_id))

        return db.Execute("SELECT amount FROM com_upgrade WHERE tag='{id}' AND upgrade_id='{upgrade_id}'".format(
            id=self.__company_tag, upgrade_id=upgrade_id))[0][0]

    def get_upgrade(self, upgrade_id):
        return db.Execute("SELECT amount FROM com_upgrade WHERE tag='{tag}' AND upgrade_id={upgrade_id}".format(tag=self.__company_tag, upgrade_id=upgrade_id))

    def add_upgrade(self, upgrade_id, value=1):
        r = db.Execute("""SELECT * FROM com_upgrade WHERE tag = '{tag}' AND upgrade_id='{upgrade_id}'""".format(
            tag=self.__company_tag, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO com_upgrade(tag, upgrade_id) VALUES('{tag}', '{upgrade_id}')".format(
                tag=self.__company_tag, upgrade_id=upgrade_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE com_upgrade SET amount = amount + '{value}' WHERE tag = '{tag}' AND upgrade_id='{upgrade_id}';""".format(
                tag=self.__company_tag, value=value, upgrade_id=upgrade_id))

    def remove_upgrade(self, upgrade_id, value=1):
        r = db.Execute("""SELECT * FROM com_upgrade WHERE tag = '{tag}' AND upgrade_id='{upgrade_id}'""".format(
            tag=self.__company_tag, upgrade_id=upgrade_id))
        if not r:
            db.Execute("INSERT INTO com_upgrade(tag, upgrade_id) VALUES('{tag}', '{upgrade_id}')".format(
                tag=self.__company_tag, value=value, upgrade_id=upgrade_id))

        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        return db.Execute(
            """UPDATE com_upgrade SET amount = amount - '{value}' WHERE tag = '{tag}' AND upgrade_id='{upgrade_id}';""".format(
                tag=self.__company_tag, value=value, upgrade_id=upgrade_id))

    def add_role(self, user_id, role):
        self.remove_role(user_id)
        db.Execute(f"INSERT INTO com_roles(id, tag, role) VALUES('{user_id}', '{self.__company_tag}', '{role}')")

    def remove_role(self, user_id):
        db.Execute(f"""DELETE FROM com_roles WHERE id='{user_id}'""")

    def get_required_exp(self):
        return config.exp_per_level * self.get_level() * self.get_level() * 5

    def get_exp(self):
        return int(db.Execute("SELECT exp FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def deduct_exp(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "exp", value, self.__company_tag, "tag")

    def add_exp(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "exp", value, self.__company_tag, "tag")

    def get_level(self):
        return int(db.Execute("SELECT level FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def deduct_level(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "level", value, self.__company_tag, "tag")

    def add_level(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "level", value, self.__company_tag, "tag")

    def get_income(self):
        income = int(db.Execute("SELECT income FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])
        income += self.get_modules_total_income()
        return income

    def deduct_income(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "income", value, self.__company_tag, "tag")

    def add_income(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "income", value, self.__company_tag, "tag")

    def get_capacity(self):
        capacity = int(db.Execute("SELECT capacity FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])
        capacity += self.get_modules_total_capacity()
        return capacity

    def deduct_capacity(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "capacity", value, self.__company_tag, "tag")

    def add_capacity(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "capacity", value, self.__company_tag, "tag")

    def get_max_cap(self):
        return int(db.Execute("SELECT max_cap FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def deduct_max_cap(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "max_cap", value, self.__company_tag, "tag")

    def add_max_cap(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "max_cap", value, self.__company_tag, "tag")

    def get_total_sold(self):
        return int(db.Execute("SELECT total_sold FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def deduct_total_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "total_sold", value, self.__company_tag, "tag")

    def add_total_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "total_sold", value, self.__company_tag, "tag")

    def get_income_sold(self):
        return int(db.Execute("SELECT income_sold FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def deduct_income_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Deduct("company", "income_sold", value, self.__company_tag, "tag")

    def add_income_sold(self, value):
        try:
            value = int(value)
            if value < 0:
                value = 0
        except:
            value = 0

        db.Addition("company", "income_sold", value, self.__company_tag, "tag")

    def total_members(self):
        return len(db.Execute(f"SELECT * FROM com_roles WHERE tag='{self.__company_tag}'"))

    def self_delete(self):
        tables = db.GetAllTables()
        for x in tables:
            try:
                db.Execute(f"""DELETE FROM {x} WHERE tag='{self.get_tag()}';""")
            except:
                pass

    def reset_tax_time(self):
        db.Update("company", "tax_return", str(round(time.time())), self.__company_tag, "tag")

    def get_tax_time(self):
        return int(db.Execute("SELECT tax_return FROM company WHERE tag='{tag}'".format(tag=self.__company_tag))[0][0])

    def get_modules(self):
        r = []
        list = db.Execute("SELECT module_id FROM com_modules WHERE tag='{tag}'".format(tag=self.__company_tag))
        for x in list:
            r.append(x[0])

        return r

    def add_modules(self, module_id, income=0, capacity=0):

        list = db.Execute(
            "SELECT module_id FROM com_modules WHERE tag='{tag}' AND module_id='{module_id}'".format(tag=self.__company_tag,
                                                                                             module_id=module_id))
        if list:
            return

        return db.Execute(
            f"INSERT INTO com_modules(tag, module_id, income, capacity) VALUES('{self.__company_tag}', '{module_id}', '{income}', '{capacity}')")

    def get_modules_income(self, module_id):
        try:
            value = db.Execute(
                f"SELECT income FROM com_modules WHERE module_id='{module_id}' AND tag='{self.__company_tag}'")[
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

        return db.Execute(
            f"UPDATE com_modules SET income = income + '{value}' WHERE tag = '{self.__company_tag}' AND module_id='{module_id}';")

    def get_modules_capacity(self, module_id):
        try:
            value = db.Execute(
                f"SELECT capacity FROM com_modules WHERE module_id='{module_id}' AND tag='{self.__company_tag}'")[
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

        return db.Execute(
            f"UPDATE com_modules SET capacity = capacity + '{value}' WHERE tag = '{self.__company_tag}' AND module_id='{module_id}';")

    def get_modules_total_income(self):
        try:
            value = db.Execute(
                f"SELECT sum(income) FROM com_modules WHERE tag='{self.__company_tag}'")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def get_modules_total_capacity(self):
        try:
            value = db.Execute(
                f"SELECT sum(capacity) FROM com_modules WHERE tag='{self.__company_tag}'")[
                0][0]

            if not value:
                return 0

            return value
        except:
            return 0

    def get_available_upgrades(self):
        return list(data["company"]["upgrade"].keys())