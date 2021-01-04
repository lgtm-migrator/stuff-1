import asyncio
import aiohttp


async def duck_search(search_term):
    search_term = "+".join(search_term.split())
    url = f"https://api.duckduckgo.com/?q={search_term}&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                content = await r.json(content_type="application/x-javascript")
                result = content["AbstractText"]
                if content["AbstractText"] == "":
                    result = content["RelatedTopics"][0]["Text"]
                return result


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(duck_search(input("> ")))
