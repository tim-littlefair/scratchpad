# Examples based on  https://docs.python.org/3/library/asyncio-task.html

import asyncio
import collections
import os
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
    async def create_subprocess_task(self,subprocess_tag, subprocess_cmd):
        task = self.create_task(self._create_subprocess(subprocess_tag, subprocess_cmd))
    async def _create_subprocess(self,subprocess_tag, subprocess_cmd):
        proc=None
        if os.path.exists(subprocess_cmd):
            raise NotImplementedError
        else:
            proc = await asyncio.create_subprocess_shell(
                subprocess_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                # We would prefer text=True for this application, but
                # a.c_s_s raises ValueError => required value made explicit
                text=False,
            )
        self.subprocess_map[subprocess_tag]=proc
    async def sp_read(self,tag):
        p = self.subprocess_map[tag]
        return await p.stdout.read()
    async def wait_for_processes(self):
        for k in self.subprocess_map.keys():
            p = self.subprocess_map[k]
            output = await self.sp_read(k)
            print(f"Output on {k}>>>\n{output.decode()}\n<<<")
            print(f"Waiting for {k}", flush=True)
            await p.wait()


async def main_v4():
    async with SubprocessTaskGroup() as tg:
        task1 = await tg.create_subprocess_task("task1", "sleep 1 ; echo 1")
        task2 = await tg.create_subprocess_task("task2", "sleep 2 ; echo 2")
        print(f"started at {time.strftime('%X')}")
        timeout=1.0 # 0.001 not enough, 0.1 seems to be enough
        await asyncio.sleep(timeout)
        await tg.wait_for_processes()

    # The await is implicit when the context manager exits.
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main_v4())
