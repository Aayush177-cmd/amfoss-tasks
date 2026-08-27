import discord
from discord.ext import commands
import asyncio
import os

import database

print(database.__file__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    print("Registered commands:")

    for command in bot.commands:
        print(command.name)


@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    await bot.process_commands(message)


async def main():
    print("Calling initialize_database()")
    database.initialize_database()
    print("Finished initialize_database()")
    print("Database initialized")


    database.initialize_shop()
    print("Shop initialized")

    async with bot:
        await bot.load_extension("commands.economy")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())