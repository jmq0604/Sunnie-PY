import time

from classes.user import UserData
from classes import base_command
from globals import *
from helper import helper


class Command(base_command.BaseCMD):
    def __init__(self):
        self.name = "transfer"
        self.cmd = ["t", "give"]
        self.args = True
        self.help = "[user] [amount]"
        self.category = "Bank"
        self.description = "Transfer money to another user while paying a bank fee"

        base_command.BaseCMD.__init__(self, self.cmd, self.name, self.help, 7200)

    async def run(self, client, message, clean, user=UserData()):
        prefix = user.get_prefix()
        if not user.has_bank():
            return await message.reply(embed=helper.embed(message, "Bank Transfer",
                                                          "{e} You are **required** to open a bank account before being able to transfer cash to another user! Do so by using the `{p}bank` command and opening an account".format(
                                                              e=data["emotes"]["cross"], p=prefix)))

        if len(clean) < 2:
            return await message.reply(embed=helper.embed(message, "Bank Transfer",
                                                          "{e} Please use the correct format, `{p}transfer <user> <amount>` next time!".format(
                                                              e=data["emotes"]["cross"], p=prefix)))

        user_receive = helper.clean_message(clean[0])

        try:
            amount = int(helper.clean_message(clean[1]))
        except:
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   ":x: Please enter a **valid number** next time!"))

        if amount < 10:
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   ":x: You are **unable** to send cash less than `1,000`!"))

        if not db.Exist("users", "id", user_receive):
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   f":x: The person **does not seem** to be in our database, please make sure they have done `{prefix}startup`!"))

        if str(user_receive) == str(message.author.id):
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   ":x: You are **unable** to send cash to yourself!"))

        user_receive = UserData(user_receive)
        if amount > data['banks'][user.get_bank()]["price"]:
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   f":x: Due to your bank, you **are unable** to send more than `{helper.money(data['banks'][user.get_bank()]['price'])}`!"))

        if user.get_bank_money() < amount:
            return await message.reply(
                embed=helper.embed(message, f"Bank Transfer",
                                   f":x: You currently **do not have** that amount in your bank! You can deposit money using `{prefix}dep <amount>`!"))

        fee = int(float(amount) / 100.0 * 5.0)
        user.deduct_bank_money(amount)
        user_receive.add_money(int(amount - fee))

        user.statistics.add_transferred(amount)
        user_receive.statistics.add_recevied(int(amount - fee))

        embeds = {}
        embeds["Sent"] = f"`${helper.money(amount)}`"
        embeds["Bank Fees"] = f"`${helper.money(fee)}`"
        embeds["Received"] = f"`${helper.money((int(amount - fee)))}`"

        return await message.reply(
            embed=helper.embed(message, f"Bank Transfer | Sent", f" ", embeds=embeds, inline=True))










commands.append(Command())
