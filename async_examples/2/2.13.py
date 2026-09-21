# Защита задачи от снятия
import asyncio
from async_examples.utils.delay_functions import delay

async def main():
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("задача заняла более 5 сек")
        result = await task
        print(result)

asyncio.run(main())