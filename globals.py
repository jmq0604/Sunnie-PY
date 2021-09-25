from helper import database
import json

db = database.database()

words = open("./assets/wordlist.txt").read().splitlines()
data = json.load(open('./data.json',))
commands = []
commands_dict = {}
sql_commands = []

employees = {}
user_cooldown = {}
user_ingame = {}

daily_tasks = {}
task_completion = {}