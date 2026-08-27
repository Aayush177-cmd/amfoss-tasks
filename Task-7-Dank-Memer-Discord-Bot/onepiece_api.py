import aiohttp

BASE_URL = "https://api.api-onepiece.com/v2"


async def get_character(name):

    url = f"{BASE_URL}/characters/en"

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as response:

            if response.status != 200:
                print("API ERROR:", response.status)
                return None

            data = await response.json()

            print("API RESPONSE:", data)

            # Search through the returned characters
            for character in data:

                character_name = character.get("name", "")

                if name.lower() in character_name.lower():
                    return character

    return None