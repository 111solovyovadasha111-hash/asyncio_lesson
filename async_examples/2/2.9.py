import asyncio
from async_examples.utils.delay_functions import delay

async def main():
    sleep_for_three = asyncio.create_task(delay(4))  # а тут
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    await sleep_for_three # останавливаемся здесь
    await sleep_again # останавливаемся здесь
    await sleep_once_more # останавливаемся здесь
asyncio.run(main())