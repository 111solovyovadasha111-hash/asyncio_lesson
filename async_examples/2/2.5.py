import asyncio

async def hello_world_message() -> str:
    await asyncio.sleep(1) # Приостановить hello_world_message на 1 с
    return 'Hello World!'

async def main() -> None:
    message = await hello_world_message()
    print(message)

asyncio.run(main())