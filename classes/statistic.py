from classes.server import *


class Statistics:
    def __init__(self, user_id):
        self.__id = user_id
        self.__stats = db.Retrieve("statistic", "id", self.__id)
        self.__keys = db.GetTableColumn("statistic")

    def __getitem__(self, key):
        if not str(key).isdigit():
            key =  self.__keys.index(key)

        return self.__stats[key]

    def get_id(self):
        return self.__id

    def get_deposit(self):
        return self["total_deposit"]

    def add_deposit(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_deposit = total_deposit + '{value}' WHERE id = '{self.__id}';")

    def get_recevied(self):
        return self["total_received"]

    def add_recevied(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_received = total_received + '{value}' WHERE id = '{self.__id}';")

    def get_transferred(self):
        return self["total_transferred"]

    def add_transferred(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_transferred = total_transferred + '{value}' WHERE id = '{self.__id}';")

    def get_gambling_lost(self):
        return self["total_gambling_lost"]

    def add_gambling_lost(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_gambling_lost = total_gambling_lost + '{value}' WHERE id = '{self.__id}';")

    def get_gambling_won(self):
        return self["total_gambling_won"]

    def add_gambling_won(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_gambling_won = total_gambling_won + '{value}' WHERE id = '{self.__id}';")

    def get_gambling_commands(self):
        return self["total_gambling_commands"]

    def add_gambling_commands(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(
            f"UPDATE statistic SET total_gambling_commands = total_gambling_commands + '{value}' WHERE id = '{self.__id}';")

    def get_skills(self):
        return self["total_skills"]

    def add_skills(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_skills = total_skills + '{value}' WHERE id = '{self.__id}';")

    def get_tips(self):
        return self["total_tips"]

    def add_tips(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_tips = total_tips + '{value}' WHERE id = '{self.__id}';")

    def get_work(self):
        return self["total_work"]

    def add_work(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_work = total_work + '{value}' WHERE id = '{self.__id}';")

    def get_spent(self):
        return self["total_spent"]

    def add_spent(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_spent = total_spent + '{value}' WHERE id = '{self.__id}';")

    def get_income(self):
        return self["total_income"]

    def add_income(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_income = total_income + '{value}' WHERE id = '{self.__id}';")

    def get_votes(self):
        return self["total_votes"]

    def add_votes(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_votes = total_votes + '{value}' WHERE id = '{self.__id}';")

    def get_commands(self):
        return self["total_commands"]

    def add_command(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_commands = total_commands + '{value}' WHERE id = '{self.__id}';")

    def get_daily(self):
        return self["total_daily"]

    def add_daily(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_daily = total_daily + '{value}' WHERE id = '{self.__id}';")

    def get_interest(self):
        return self["total_interest"]

    def add_interest(self, value=1):
        try:
            value = int(value)
        except:
            value = 0

        return db.Execute(f"UPDATE statistic SET total_interest = total_interest + '{value}' WHERE id = '{self.__id}';")
