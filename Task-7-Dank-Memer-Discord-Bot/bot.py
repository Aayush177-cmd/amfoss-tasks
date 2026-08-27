import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

import database


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(
    dotenv_path=os.path.join(BASE_DIR, ".env")
)

TOKEN = os.getenv("DISCORD_TOKEN")

print("Token loaded:", TOKEN is not None)


intents = discord.Intents.default()

intents.message_content = True
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print()
    print("------------------------------")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("------------------------------")

    print("\nRegistered commands:")

    for command in bot.commands:
        print("-", command.name)

    print()


@bot.event
async def on_message(message):

    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    print(
        f"Message received from "
        f"{message.author}: "
        f"{message.content}"
    )

    await bot.process_commands(message)


async def main():

    print("Starting Berry Broker...")

    if not TOKEN:
        print("ERROR: DISCORD_TOKEN is not set.")
        print("Check your .env file.")
        return

    print("\nInitializing database...")

    database.initialize_database()

    print("Database initialized.")

    # Initialize shop
    database.initialize_shop()

    print("Shop initialized.")

    async with bot:

        print("\nLoading Economy extension...")

        await bot.load_extension(
            "commands.economy"
        )

        print("Economy extension loaded.")

        print("\nStarting Discord bot...\n")

        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())