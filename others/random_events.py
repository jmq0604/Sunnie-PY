import asyncio
import random

from classes.server import *
from others import mini_games


async def start_event(client, message):
    if random.randint(0, 200) < config.event_chance:
        try:
            title = ":white_check_mark: Task Completed"
            body = "A random **EVENT** has started! Completed the task below to win a price!"

            chance = random.randint(1, 2)
            if chance == 1:
                await mini_games.unscramble(client, message, title, body, True)
            elif chance == 2:
                await mini_games.pharse(client, message, title, body, True)

            return

        except asyncio.TimeoutError:
            return await message.reply(
                embed=helper.embed(message, ":x: Event In-Completed",
                                   "No one completed the event. Better luck next time, the customers left!"))