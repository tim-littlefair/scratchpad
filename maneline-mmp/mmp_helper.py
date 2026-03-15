# Examples based on  https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main_v1():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

async def main_v2():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

async def main_v3():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")

class SubprocessTaskGroup(asyncio.TaskGroup):
    def __init__(self):
        super().__init__()
        self.subprocess_map = {}

async def main_v4():
    async with SubprocessTaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'stg-hello'))

        task2 = tg.create_task(
            say_after(2, 'stg-world'))

        print(f"started at {time.strftime('%X')}")

    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")




asyncio.run(main_v4())
