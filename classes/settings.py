import math, random, time, config

from helper import helper
from globals import *

from classes.server import ServerData
from classes.statistic import Statistics
from classes.company import CompanyData


class SettingsData:
    def __init__(self, user_id=None):
        self.__userid = str(user_id).strip()

    def set_settings(self, setting_id, value):
        r = db.Execute(
            "SELECT value FROM settings WHERE id={id} AND settings_id='{setting_id}'".format(id=self.__userid, setting_id=setting_id))
        if not r:
            return db.Execute(
                "INSERT INTO settings(id, settings_id, value) VALUES('{id}', '{setting_id}', '{v}')".format(
                    id=self.__userid, v=value, setting_id=setting_id))

        db.Execute("""UPDATE settings SET value = '{value}' WHERE id = '{id}' AND settings_id='{setting_id}';""".format(
            id=self.__userid, value=value, setting_id=setting_id))

    def get_interaction(self):
        r = db.Execute("SELECT value FROM settings WHERE id={id} AND settings_id='interaction'".format(id=self.__userid))
        if not r:
            db.Execute("INSERT INTO settings(id, settings_id, value) VALUES('{id}', 'interaction', '0')".format(
                id=self.__userid))
            return False

        return bool(r[0][0])

    def set_interaction(self, value):
        r = db.Execute("SELECT value FROM settings WHERE id={id} AND settings_id='interaction'".format(id=self.__userid))
        if not r:
            return db.Execute("INSERT INTO settings(id, settings_id, value) VALUES('{id}', 'interaction', '{v}')".format(
                id=self.__userid, v=value))


        db.Execute("""UPDATE settings SET value = '{value}' WHERE id = '{id}' AND settings_id='interaction';""".format(
                id=self.__userid, value=value))

    def presettings(self):
        self.get_interaction()

    def all_settings(self):
        return db.Execute("SELECT settings_id, value FROM settings WHERE id={id}".format(id=self.__userid))
