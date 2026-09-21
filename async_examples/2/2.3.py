
import asyncio

async def coroutine_add_one(number: int) -> int:
    return number + 1

result = asyncio.run(coroutine_add_one(1)) # главная точка входа в созданное нами приложение asyncio
# создает новое событие
# выполняет код переданной нами сопрограммы до конца и возвращает результат
print(result)