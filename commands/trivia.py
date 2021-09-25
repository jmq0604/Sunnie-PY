import asyncio
import random

import config
from classes import base_command
from globals import *
from helper import helper

from others import mini_games


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "trivia"
        self.cmd = ["tr", "questions"]
        self.args = False
        self.help = ""
        self.cooldown = 300
        self.category = "Basic"
        self.description = "Play a mini-game which tests your knowledge on food"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, self.cooldown)

    async def run(self, client, message, clean, user):
        prefix = user.get_prefix()

        body = "Please answer the question below in **20 seconds**. Reply with **just the letter** of the answer you think is right!\n\n"

        question = list(data["minigame"]["trivia"]["questions"])
        question = random.choice(question)

        body += f"**{question['question']}**\n"
        for x in range(len(question["choices"])):
            body += question["choices"][x] + "\n"

        await message.reply(
            embed=helper.embed(message, "<:AquaYeah:857292255122423809> Trivia Night!", body))

        def check(m):
            if m.author.id == message.author.id:
                return True
            return False

        try:
            msg = await client.wait_for('message', check=check, timeout=20)
            answer = helper.clean_message(msg.content).lower()
            if answer == question["correct"]:

                body = "Nicely Done! You won yourself "
                body = mini_games.random_reward_2(body, "Nicely done, keep it up!", user)

                user.add_exp(random.randint(1, 50))
                return await message.reply(
                    embed=helper.embed(message, "<:bAm:857283904510361610> Trivia Passed", body, footer=" "))
            else:
                return await message.reply(
                    embed=helper.embed(message, ":x: Trivia Failed",
                                       "Your answer was wrong! Please try harder next time!", footer=" "))

        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Trivia Incomplete",
                                   "You ran out of time! Better luck next time, your customers left.".format(p=prefix)))


commands.append(Command())
