from discord.ext import commands
import discord
import time
import database
import onepiece_api
from onepiece_api import get_character

DAILY_REWARD = 500
DAILY_COOLDOWN = 24 * 60 * 60
RAID_COOLDOWN = 60 * 60

FRUIT_BONUSES = {
    "Gomu_Gomu_no_Mi": 100,
    "Mera_Mera_no_Mi": 200,
    "Ope_Ope_no_Mi": 300,
    "Gura_Gura_no_Mi": 500
}


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("Economy Cog Loaded")

    @commands.command()
    async def bounty(self, ctx):

        print("BOUNTY COMMAND CALLED")

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        wallet = user["wallet"]
        bank = user["bank"]
        total = wallet + bank

        await ctx.send(
            f"**{user['username']}'s Bounty**\n"
            f"Wallet: **{wallet} Berries**\n"
            f"Bank: **{bank} Berries**\n"
            f"Total Wealth: **{total} Berries**"
        )

    @commands.command()
    async def setsail(self, ctx):

        print("SETSAIL COMMAND CALLED")

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        current_time = int(time.time())
        last_daily = user["last_daily"]

        if current_time - last_daily < DAILY_COOLDOWN:

            remaining = DAILY_COOLDOWN - (
                current_time - last_daily
            )

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            await ctx.send(
                f"You have already claimed your daily Berries!\n"
                f"Try again in **{hours}h {minutes}m**."
            )

            return

        new_wallet = user["wallet"] + DAILY_REWARD

        database.update_wallet(
            user["user_id"],
            new_wallet
        )

        database.update_last_daily(
            user["user_id"],
            current_time
        )

        await ctx.send(
            f"**You set sail and raided a merchant ship!**\n"
            f"You received **{DAILY_REWARD} Berries**!\n"
            f"New Wallet Balance: **{new_wallet} Berries**"
        )

    @commands.command()
    async def trade(self, ctx, member_id: int, amount: int):

        print("TRADE COMMAND CALLED")

        try:
            member = await ctx.guild.fetch_member(member_id)
        except discord.NotFound:
            await ctx.send("User not found.")
            return

        sender = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        receiver = database.get_or_create_user(
            member.id,
            member.name
        )

        database.transfer_berries(
            sender["user_id"],
            receiver["user_id"],
            amount
        )

        await ctx.send(
            f"{ctx.author.mention} sent "
            f"{amount} Berries to {member.mention}"
        )




    @commands.command()
    async def deposit(self, ctx, amount: int):

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        wallet = user["wallet"]
        bank = user["bank"]

        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return

        if wallet < amount:
            await ctx.send("You don't have enough Berries.")
            return

        wallet -= amount
        bank += amount

        database.update_wallet(
            user["user_id"],
            wallet
        )

        database.update_bank(
            user["user_id"],
            bank
        )

        await ctx.send(
            f"Deposited **{amount} Berries**.\n"
            f"Wallet: **{wallet}**\n"
            f"Bank: **{bank}**"
        )




    @commands.command()
    async def withdraw(self, ctx, amount: int):

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        wallet = user["wallet"]
        bank = user["bank"]

        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return

        if bank < amount:
            await ctx.send("You don't have enough Berries in the bank.")
            return

        wallet += amount
        bank -= amount

        database.update_wallet(
            user["user_id"],
            wallet
        )

        database.update_bank(
            user["user_id"],
            bank
        )

        await ctx.send(
            f"Withdrew **{amount} Berries**.\n"
            f"Wallet: **{wallet}**\n"
            f"Bank: **{bank}**"
        )

    @commands.command()
    async def worstgeneration(self, ctx):

        users = database.get_top_users()

        message = " **Worst Generation Leaderboard** \n\n"

        for index, user in enumerate(users, start=1):

            total = user["wallet"] + user["bank"]

            message += (
                f"{index}. "
                f"{user['username']} — "
                f"{total} Berries\n"
            )

        await ctx.send(message)

    @commands.command()
    async def shop(self, ctx):

        print("SHOP COMMAND IS CALLED")

        items = database.get_shop_items()


        print(items)

        message = " **Berry Broker Shop** \n\n"

        for item in items:
            message += (
                f"**{item['name']}**\n"
                f"Price: {item['price']} Berries\n"
                f"{item['description']}\n\n"
            )

        await ctx.send(message)

    @commands.command()
    async def buy(self, ctx, *, item_name):

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        item = database.get_item(item_name)

        if item is None:
            await ctx.send("Item not found.")
            return

        if user["wallet"] < item["price"]:
            await ctx.send("You don't have enough Berries.")
            return

        database.update_wallet(
            user["user_id"],
            user["wallet"] - item["price"]
        )

        database.add_item_to_inventory(
            user["user_id"],
            item["name"]
        )

        await ctx.send(
            f"You bought **{item['name']}**!"
        )

    @commands.command()
    async def inventory(self, ctx):

        items = database.get_inventory(
            ctx.author.id
        )

        if len(items) == 0:
            await ctx.send("Your inventory is empty.")
            return

        message = "**Inventory**\n\n"

        for item in items:
            message += (
                f"{item['item_name']} "
                f"(x{item['quantity']})\n"
            )

        await ctx.send(message)

    @commands.command()
    async def raid(self, ctx, member_id: int):

        if member_id == ctx.author.id:
            await ctx.send("You cannot raid yourself.")
            return

        try:
            member = await ctx.guild.fetch_member(member_id)
        except discord.NotFound:
            await ctx.send("User not found.")
            return

        attacker = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        victim = database.get_or_create_user(
            member.id,
            member.name
        )

        current_time = int(time.time())

        if current_time - attacker["last_raid"] < RAID_COOLDOWN:
            await ctx.send("Your crew needs more time to prepare.")
            return

        fruit = database.get_fruit(attacker["user_id"])

        bonus = 0

        if fruit is not None:
            bonus = FRUIT_BONUSES.get(
                fruit["fruit_name"],
                0
            )

        stolen = min(
            200 + bonus,
            victim["wallet"]
        )

        if stolen == 0:
                    await ctx.send("The target has no Berries.")
                    return

        database.update_wallet(
            attacker["user_id"],
            attacker["wallet"] + stolen
        )

        database.update_wallet(
            victim["user_id"],
            victim["wallet"] - stolen
        )

        database.update_last_raid(
            attacker["user_id"],
            current_time
        )

        await ctx.send(
        f"{ctx.author.mention} stole "
        f"**{stolen}** Berries!"
        )


    @commands.command()
    async def buyship(self, ctx, *, ship_name):

        if ship_name not in database.SHIP_DATA:
            await ctx.send(
                "That ship does not exist."
            )
            return

        user = database.get_or_create_user(
            ctx.author.id,
            ctx.author.name
        )

        ship_data = database.SHIP_DATA[ship_name]
        price = ship_data["price"]

        if user["wallet"] < price:
            await ctx.send(
                f"You need **{price} Berries** to buy "
                f"the **{ship_name}**."
            )
            return

        database.update_wallet(
            ctx.author.id,
            user["wallet"] - price
        )

        database.create_ship(
            ctx.author.id,
            ship_name
        )

        await ctx.send(
            f"{ctx.author.mention} bought a "
            f"**{ship_name}** for **{price} Berries**!"
        )

    @commands.command()
    async def myship(self, ctx):

        ship = database.get_ship(ctx.author.id)

        if ship is None:
            await ctx.send("You don't own a ship.")
            return

        await ctx.send(
            f"🚢 **{ship['ship_name']}**\n"
            f"Health: {ship['health']}\n"
            f"Attack: {ship['attack']}"
        )

    @commands.command()
    async def createcrew(self, ctx, *, name):

            database.create_crew(
                name,
                ctx.author.id
            )

            await ctx.send(
                f"🏴‍☠️ Crew **{name}** has been created!"
            )

    

    @commands.command()
    async def crewleaderboard(self, ctx):

        crews = database.get_top_crews()

        if len(crews) == 0:
            await ctx.send("No crews have been created.")
            return

        message = "🏴‍☠️ **Crew Leaderboard**\n\n"

        for index, crew in enumerate(crews, start=1):
            message += (
                f"{index}. "
                f"{crew['name']} "
                f"({crew['members']} members)\n"
            )

        await ctx.send(message)


    @commands.command()
    async def eat(self, ctx, *, fruit_name):

        existing_fruit = database.get_fruit(
            ctx.author.id
        )

        if existing_fruit is not None:
            await ctx.send(
                "You already possess a Devil Fruit."
            )
            return

        database.give_fruit(
            ctx.author.id,
            fruit_name
        )

        await ctx.send(
            f"{ctx.author.mention} ate the "
            f"**{fruit_name}**!"
        )

    @commands.command()
    async def fruit(self, ctx):

        fruit = database.get_fruit(
            ctx.author.id
        )

        if fruit is None:
            await ctx.send(
                "You don't have a Devil Fruit."
            )
            return

        await ctx.send(
            f"Your Devil Fruit is "
            f"**{fruit['fruit_name']}**."
        )


    @commands.command()
    async def removefruit(self, ctx):

        database.remove_fruit(
            ctx.author.id
        )

        await ctx.send(
            "Your Devil Fruit has been removed."
        )


    @commands.command()
    async def battle(self, ctx, member: discord.Member):

            if member.id == ctx.author.id:
                await ctx.send("You cannot battle yourself.")
                return

            player_ship = database.get_ship(ctx.author.id)
            enemy_ship = database.get_ship(member.id)

            if player_ship is None:
                await ctx.send("You don't have a ship.")
                return

            if enemy_ship is None:
                await ctx.send(
                    f"{member.display_name} doesn't have a ship."
                )
                return

            player_health = player_ship["health"]
            enemy_health = enemy_ship["health"]

            player_attack = player_ship["attack"]
            enemy_attack = enemy_ship["attack"]

            battle_log = (
                f"Ship Battle!\n\n"
                f"{ctx.author.mention}: "
                f"**{player_ship['ship_name']}**\n"
                f"Health: {player_health} | Attack: {player_attack}\n\n"
                f"{member.mention}: "
                f"**{enemy_ship['ship_name']}**\n"
                f"Health: {enemy_health} | Attack: {enemy_attack}\n\n"
            )

            turn = 1

            while player_health > 0 and enemy_health > 0:

                # Player attacks
                enemy_health -= player_attack

                battle_log += (
                    f"Turn {turn}: "
                    f"{ctx.author.display_name}'s ship attacks "
                    f"for {player_attack} damage.\n"
                )

                if enemy_health <= 0:
                    break

                # Enemy attacks
                player_health -= enemy_attack

                battle_log += (
                    f"Turn {turn}: "
                    f"{member.display_name}'s ship attacks "
                    f"for {enemy_attack} damage.\n"
                )

                turn += 1

            if player_health > 0:
                winner = ctx.author.mention
                winning_ship = player_ship["ship_name"]
            else:
                winner = member.mention
                winning_ship = enemy_ship["ship_name"]

            battle_log += (
                f"\nThe battle is over!\n"
                f"Winner: {winner}\n"
                f"Winning Ship: **{winning_ship}**"
            )

            await ctx.send(battle_log)


    @commands.command()
    async def joincrew(self, ctx, crew_name):

        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT crew_id
            FROM crews
            WHERE name = ?
            """,
            (crew_name,)
        )

        crew = cursor.fetchone()

        if crew is None:
            await ctx.send("Crew not found.")
            connection.close()
            return

        cursor.execute(
            """
            INSERT OR IGNORE INTO crew_members
            VALUES (?, ?)
            """,
            (crew["crew_id"], ctx.author.id)
        )

        connection.commit()
        connection.close()

        await ctx.send(
            f"{ctx.author.mention} joined **{crew_name}**!"
        )

    @commands.command()
    async def crewmembers(self, ctx, *, crew_name):

        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT users.username
            FROM crew_members
            JOIN users
            ON crew_members.user_id = users.user_id
            JOIN crews
            ON crew_members.crew_id = crews.crew_id
            WHERE crews.name = ?
            """,
            (crew_name,)
        )

        members = cursor.fetchall()

        connection.close()

        if len(members) == 0:
            await ctx.send("Crew not found.")
            return

        message = f" **{crew_name} Members**\n\n"

        for member in members:
            message += f" {member['username']}\n"

        await ctx.send(message)



    @commands.command()
    async def mycrew(self, ctx):

        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT crews.name
            FROM crews
            JOIN crew_members
            ON crews.crew_id = crew_members.crew_id
            WHERE crew_members.user_id = ?
            """,
            (ctx.author.id,)
        )

        crew = cursor.fetchone()

        connection.close()

        if crew is None:
            await ctx.send("You are not part of a crew.")
            return

        await ctx.send(f"You belong to **{crew['name']}**.")

    @commands.command()
    async def leavecrew(self, ctx):

        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM crew_members
            WHERE user_id = ?
            """,
            (ctx.author.id,)
        )

        connection.commit()
        connection.close()

        await ctx.send(
            f"{ctx.author.mention} has left the crew."
        )    
    @commands.command()
    async def repairship(self, ctx):

        ship = database.get_ship(ctx.author.id)

        if ship is None:
            await ctx.send("You don't own a ship.")
            return

        full_health = database.SHIP_DATA[
            ship["ship_name"]
        ]["health"]

        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE ships
            SET health = ?
            WHERE user_id = ?
            """,
            (full_health, ctx.author.id)
        )

        connection.commit()
        connection.close()

        await ctx.send(
            f" Your **{ship['ship_name']}** has been repaired!"
        )
    @commands.command()
    async def helpme(self, ctx):

            message = """
            
    **BERRY BROKER COMMANDS**

    **ECONOMY**

    !bounty - View your Berries
    !setsail - Claim daily Berries
    !deposit <amount> - Deposit Berries
    !withdraw <amount> - Withdraw Berries
    !trade <member_id> <amount> - Send Berries
    !worstgeneration - View the richest pirates

    **SHOP**

    !shop - View the shop
    !buy <item> - Buy an item
    !inventory - View your inventory

    **CREWS**

    !createcrew <name> - Create a crew
    !joincrew <name> - Join a crew
    !leavecrew - Leave your crew
    !mycrew - View your crew
    !crewmembers - View crew members
    !crewleaderboard - Top crews

    **DEVIL FRUITS**

    !eat <fruit> - Eat a Devil Fruit
    !fruit - View your Devil Fruit
    !removefruit - Remove your Devil Fruit


    **SHIPS**


    !buyship <name> - Buy a ship
    !myship - View your ship
    !repairship - Repair your ship
    !battle @member - Battle another pirate


    **ONE PIECE DATABASE**

    !character <name> - Search for a One Piece character


    Use these commands to become the next Pirate King!
    """

            await ctx.send(message)    
        
    @commands.command()
    async def character(self, ctx, *, name):

        await ctx.send(
            f"Searching the One Piece database for **{name}**..."
        )

        data = await get_character(name)

        if not data:
            await ctx.send("Character not found.")
            return

        # API returns a list of characters
        if isinstance(data, list):

            if len(data) == 0:
                await ctx.send("Character not found.")
                return

            character = data[0]

        else:
            character = data

        character_name = character.get("name", "Unknown")
        character_id = character.get("id", "Unknown")
        age = character.get("age", "Unknown")
        size = character.get("size", "Unknown")
        job = character.get("job", "Unknown")
        status = character.get("status", "Unknown")
        bounty = character.get("bounty", "Unknown")

        # Crew information
        crew = character.get("crew")

        if crew:
            crew_name = crew.get("name", "Unknown")
        else:
            crew_name = "No crew"

        # Devil Fruit information
        fruit = character.get("fruit")

        if fruit:
            fruit_name = fruit.get("name", "None")
            fruit_type = fruit.get("type", "Unknown")
        else:
            fruit_name = "None"
            fruit_type = "N/A"

        message = (
            "**One Piece Character**\n\n"
            f"**Name:** {character_name}\n"
            f"**ID:** {character_id}\n"
            f"**Age:** {age}\n"
            f"**Height:** {size}\n" 
            f"**Role:** {job}\n"
            f"**Status:** {status}\n"
            f"**Bounty:** {bounty}\n"
            f"**Crew:** {crew_name}\n"
            f"**Devil Fruit:** {fruit_name}\n"
            f"**Fruit Type:** {fruit_type}"
        )

        await ctx.send(message)         

async def setup(bot):
    await bot.add_cog(Economy(bot))