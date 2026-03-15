# Examples based on  https://docs.python.org/3/library/asyncio-task.html

import asyncio
import collections
import os
import time

class SubprocessTaskGroup(asyncio.TaskGroup):
    def __init__(self):
        super().__init__()
        self.subprocess_map = {}
    async def create_subprocess_task(self,subprocess_tag, subprocess_cmd,sleep_factor=1.0,text_io=True):
        task = self.create_task(self._create_subprocess(subprocess_tag, subprocess_cmd, sleep_factor,text_io))
    async def _create_subprocess(self,subprocess_tag, subprocess_cmd,sleep_factor, text_io):
        proc=None
        if os.path.exists(subprocess_cmd):
            raise NotImplementedError
        else:
            proc = await asyncio.create_subprocess_shell(
                subprocess_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
        proc.sleep_factor = sleep_factor
        proc.text_io = text_io
        self.subprocess_map[subprocess_tag]=proc
        await(asyncio.sleep(proc.sleep_factor))
    async def sp_read(self,tag):
        p = self.subprocess_map[tag]
        await asyncio.sleep(p.sleep_factor)
        retval = await p.stdout.read()
        if p.text_io:
            retval = retval.decode()
        return retval
    async def wait_for_processes(self):
        timeout=1.0 # 0.001 not enough, 0.1 seems to be enough
        await asyncio.sleep(timeout)
        for k in self.subprocess_map.keys():
            p = self.subprocess_map[k]
            output = await self.sp_read(k)
            print(f"Output on {k}>>>\n{output}\n<<<")
            print(f"Waiting for {k}", flush=True, end="")
            await p.wait()
            print(f" ... exited with status {p.returncode}")


async def main_v4():
    async with SubprocessTaskGroup() as tg:
        task1 = await tg.create_subprocess_task("task1", "sleep 1 ; echo 1")
        task2 = await tg.create_subprocess_task("task2", "sleep 2 ; echo 2")
        print(f"started at {time.strftime('%X')}")
        await tg.wait_for_processes()

    # The await is implicit when the context manager exits.
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main_v4())
