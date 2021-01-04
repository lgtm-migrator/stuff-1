import asyncio
import aiohttp


async def covid_data():
    url = "https://api.covid19india.org/v3/data.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                data = await r.json()
                data = data["TT"]
                added = data["delta"]
                total = data["total"]
                return added, total

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(covid_data())
