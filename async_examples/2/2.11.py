# Снятие задач
import asyncio
from asyncio import CancelledError
from async_examples.utils.delay_functions import delay

async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed= 0
    while not long_task.done():
        print('задача не закончилась')
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()
    await long_task
    # except CancelledError:
    #     print('задача снята')
    # await asyncio.sleep(2)

asyncio.run(main())