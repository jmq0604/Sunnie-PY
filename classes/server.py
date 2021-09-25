import time, re, config

from helper import helper
from globals import *


class ServerData:
    def __init__(self, server_id):
        self.__server_id = str(server_id)

        if server_id:
            db.Retrieve("servers", "id", str(server_id))

    def get_prefix(self):
        return str(db.Execute("SELECT prefix FROM servers WHERE id='{id}'".format(id=self.__server_id))[0][0])

    def set_prefix(self, prefix):
        c = db.Connection()
        c.execute("UPDATE servers SET prefix = ? WHERE id = ?", (prefix, str(self.__server_id)))
        db.Commit()

    def add_ban(self, reason="None"):
        if not db.Exist("ban_Servers", "id", self.__server_id):
            db.Execute(f"INSERT INTO ban_Servers(id, reason) VALUES('{self.__server_id}', '{reason}')")

    def remove_ban(self):
        if db.Exist("ban_Servers", "id", self.__server_id):
            db.Execute(f"""DELETE FROM ban_Servers WHERE id='{self.__server_id}';""")
