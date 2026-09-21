import asyncio
import time

async def my_coro(arg):  
    "A coroutine."
    print('before sleep')
    # await asyncio.sleep(1) 
    time.sleep(4) 
    print(arg)

async def main():  
    "The top-level coroutine." 
    a = my_coro(42)
    time.sleep(4)  
    # await asyncio.sleep(10) 
    print('before await')
    await a
    print(45)

asyncio.run(main())
