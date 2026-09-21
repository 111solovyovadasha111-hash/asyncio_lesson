import asyncio
from async_examples.utils.delay_functions import delay

async def hello_every_second():
    for i in range(4):
        await asyncio.sleep(1)
        print('пока я жду, исполняется другой код')

async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay

asyncio.run(main())

# Сначала мы запускаем две задачи, которые спят в течение 3 с; пока эти задачи простаивают,
# мы видим, как каждую секунду печатается сообщение «пока я жду, исполняется другой код!».
# Это означает, что даже во время выполнения длительных операций наше приложение может выполнять другие задачи.