# Berry Broker
Berry Broker is a Discord bot inspired by the world of One Piece. The bot allows users to earn and manage Berries, create and join pirate crews, buy ships, participate in ship battles, use Devil Fruits, and search for One Piece characters using an external API.
## Features
### Economy System
- View your Berries and total wealth
- Earn daily rewards by setting sail
- Deposit Berries into the bank
- Withdraw Berries from the bank
- Trade Berries with other users
- Raid other users
- View the Worst Generation leaderboard

### Shop and Inventory
- View available items
- Buy items using Berries
- Store purchased items in an inventory

### Pirate Crews
- Create a pirate crew
- Join an existing crew
- Leave a crew
- View your current crew
- View crew members
- View the crew leaderboard

### Devil Fruits
- Eat a Devil Fruit
- View your current Devil Fruit
- Remove your Devil Fruit
Devil Fruits can provide bonuses during raids.

### Ships
- Buy ships
- View your current ship
- Repair your ship
- Battle another player's ship

Available ships include:
- Dinghy
- Going Merry
- Thousand Sunny

### One Piece Character Search
The bot uses a One Piece API to search for character information.
The bot can display information such as:
- Character name
- Age
- Height
- Bounty
- Crew
- Devil Fruit
- Role
- Status

## Commands
### Economy
!bounty
!setsail
!deposit <amount>
!withdraw <amount>
!trade <member_id> <amount>
!raid <member_id>
!worstgeneration

### Shop
!shop
!buy <item>
!inventory

### Crews
!createcrew <name>
!joincrew <name>
!leavecrew
!mycrew
!crewmembers <crew_name>
!crewleaderboard

### Devil Fruits
!eat <fruit_name>
!fruit
!removefruit

### Ships
!buyship <ship_name>
!myship
!repairship
!battle @member

### One Piece Database
!character <name>

### Help
!helpme

## Technologies Used
- Python
- Discord.py
- SQLite
- Aiohttp
- Python-dotenv
- One Piece API

## Project Structure
Berry-Broker/
bot.py
database.py
onepiece_api.py
requirements.txt
.gitignore
commands/
economy.py
data/
services/

The following files and directories are not included in the repository:
.env
venv/
.venv/
__pycache__/
data/*.db

Activate the virtual environment:
### Linux

source venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt

## Environment Variables

Create a .env file in the root directory of the project.

Add your Discord bot token:

DISCORD_TOKEN=your_discord_bot_token_here
Do not upload your '.env' file or Discord bot token to GitHub.

## Running the Bot

Run the following command:
''
python bot.py
''

If everything is configured correctly, the bot will log in to Discord and register the available commands.

## Database

The project uses SQLite to store bot data.
The database includes tables for:
- Users
- Items
- Inventory
- Crews
- Crew Members
- Devil Fruits
- Ships

The database is automatically initialized when the bot starts.

## Example Usage

Set sail to earn Berries:
!setsail
Check your Berries and total wealth:

!bounty
View available shop items:

!shop
Buy a ship:

!buyship Going Merry
Search for a One Piece character:

!character luffy

View all available commands:

!helpme

## Future Improvements

Possible future improvements include:
- More ships and ship upgrades
- Random events
- Improved battle mechanics
- More Devil Fruit abilities
- Crew battles
- Achievements
- More advanced leaderboards
- Slash command support

## Author

Ayush Najbile
