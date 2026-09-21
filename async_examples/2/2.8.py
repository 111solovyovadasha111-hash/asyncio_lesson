import asyncio
from async_examples.utils.delay_functions import delay

async def main():
    sleep_for_three = asyncio.create_task(delay(3)) # передается подлежащая выполнению сопрограмма,
    # а в ответ она немедленно возвращает объект задачи
    print(type(sleep_for_three)) # предложение печати выполняется сразу после запуска задачи
    await sleep_for_three # а тут останавливаемся до получения результата от задачи

asyncio.run(main())

#если бы мы не включили await, то задача была бы запланирована,
# но почти сразу остановлена, после чего интерпретатор «прибрал»
# бы за ней, когда asyncio.run завершит цикл событий.