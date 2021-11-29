import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:

        pokemon_url = 'http://127.0.0.1:9996/current_user'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.text()
            print(pokemon)

asyncio.run(main())