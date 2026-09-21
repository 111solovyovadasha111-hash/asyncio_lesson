# Задание тайм-аута и снятие с помощью wait_for
import asyncio
from async_examples.utils.delay_functions import delay

async def main():
    dely_task = asyncio.create_task(delay(4))
    try:
        result = await asyncio.wait_for(dely_task, timeout=3)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("time-out")
    print(f'Задача была снята? {dely_task.cancelled()}')

asyncio.run(main())