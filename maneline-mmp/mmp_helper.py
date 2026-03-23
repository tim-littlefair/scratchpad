# Examples based on  https://docs.python.org/3/library/asyncio-task.html

import asyncio
import collections
import gc
import json
import os
import re
import sys
import time
import traceback


class SubprocessTaskGroup(asyncio.TaskGroup):
    def __init__(self):
        super().__init__()
        self.task_map = {}
        self.subprocess_map = {}
    async def create_subprocess_task(self,subprocess_tag, subprocess_cmd,timeout_factor=0.1,text_io=True):
        task = self.create_task(self._create_subprocess(subprocess_tag, subprocess_cmd, timeout_factor,text_io))
        self.task_map[subprocess_cmd]=task
    async def _create_subprocess(self,subprocess_tag, subprocess_cmd,timeout_factor, text_io):
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
        proc.timeout_factor = timeout_factor
        proc.text_io = text_io
        self.subprocess_map[subprocess_tag]=proc
    async def sp_write(self,tag, message):
        p = self.subprocess_map[tag]
        if p.text_io is True:
            message = message.encode()
        try:
            p.stdin.write(message)
            await p.stdin.drain()
            await asyncio.sleep(p.timeout_factor)
        except ConnectionResetError:
            pass
    async def sp_read(self,tag, silence_timeout=None):
        p = self.subprocess_map[tag]
        if silence_timeout is None:
            silence_timeout = p.timeout_factor
        retval = bytes()
        try:
            while(True):
                async with asyncio.timeout(silence_timeout):
                    next_chunk = await p.stdout.read()
                    if len(next_chunk)==0:
                            break
                    else:
                        retval += next_chunk
        except TimeoutError:
            pass
        if p.text_io:
            retval = retval.decode()
        return retval
    async def sp_terminate(self, tag, timeout=None):
        p = self.subprocess_map[tag]
        if p.returncode is not None:
            return
        if timeout is None:
            timeout = p.timeout_factor
        try:
            async with asyncio.timeout(timeout):
                p.terminate()
        except TimeoutError:
            pass
    async def wait_for_processes(self, timeout_factor=None):
        while len(self.subprocess_map)==0:
            print(f"Stopping process {k}",flush=True)
            p = self.subprocess_map[k]
            if timeout_factor is None:
                timeout_factor = p.timeout_factor
            try:
                subprocess_stopped = False
                p.stdin.close()
                await p.stdin.wait_closed()
                while subprocess_stopped is False:
                    async with asyncio.timeout(timeout_factor):
                        try:
                            print("Sending SIGTERM",flush=True,end="")
                            p.terminate()
                            print(" ... terminated")
                            subprocess_stopped = True
                            break
                        except TimeoutError:
                            print(" ... did not exit")
                    async with asyncio.timeout(timeout_factor):
                        try:
                            print("Sending SIGKILL",flush=True,end="")
                            p.kill()
                            print(" ... killed")
                            subprocess_stopped = True
                        except TimeoutError:
                            print(" ... did not exit")
                    break

                if True:
                    # Attempt to read any remaining data on stdout
                    try:
                        async with asyncio.timeout(timeout_factor):
                            output = await self.sp_read(k)
                            print(f"Final output on {k}>>>\n{output}\n<<<")
                    except asyncio.exceptions.CancelledError:
                        print(f"CNo final output on {k}")
                    except asyncio.exceptions.TimeoutError:
                        print(f"No final output on {k}")
                p.stdout.close()
                await p.stdout.wait_closed()
            except:
                print(f"Shutdown of subprocess {k} raised unhandled exception and might still be running)")
                traceback.print_exception(sys.exc_info()[1])
                break
            del self.subprocess_map[k]
            del self.task_map[k]

class ScriptRunner:
    def __init__(self, task_group):
        self.task_group = task_group

    def process_script_section(self, section_name, task_tag, timeout=None, only_start=False):
        global _SCRIPT_SECTIONS
        if timeout is not None:
            pass
        elif only_start is True:
            timeout = 10.0
        else:
            timeout = 1.0
        next_command = None
        response = None
        for cmd in _SCRIPT_SECTIONS.get(section_name):
            try:
                next_command = cmd.get("send", None)
                if next_command is None:
                    continue
                print(f"Sending '{next_command}'", flush=True, end="")
                expect_text = cmd.get("expect_text",None)
                task_group.sp_write(task_tag, next_command)
                if expect_text is not None:
                    response = task_group.sp_read(task_tag)
                    print(response)
                    assert expect_text in response
                else:
                    print("No response expected")
            except AssertionError:
                print(sys.exc_info()[1])
                traceback.print_tb(sys.exc_info()[2])
                break


async def get_mmp_bdaddr(task_group, tag):
    await asyncio.sleep(0.1)
    await task_group.sp_write(tag,"\n") # for output clarity
    await task_group.sp_write(tag,"scan.clear\n")
    await task_group.sp_write(tag,"scan.pattern 'Mustang Micro Plus'\n")
    await task_group.sp_write(tag,"scan le\n")
    await asyncio.sleep(2.0)
    await task_group.sp_write(tag,"scan off\n")
    await task_group.sp_write(tag,"quit\n")
    scan_output = await task_group.sp_read(tag,1.0)
    bdaddr_pattern = re.compile(r"Device ([:\d\w]+) RSSI")
    bdaddr_match = bdaddr_pattern.search(scan_output)
    if bdaddr_match is not None:
        return bdaddr_match.group(1)
    else:
        return None

async def mmp_main():
    _TAG_BTCTL = "btctl"
    print(f"started at {time.strftime('%X')}")
    async with SubprocessTaskGroup() as tg:
        btctl_task = await tg.create_subprocess_task(_TAG_BTCTL,"bluetoothctl")
        bdaddr = await get_mmp_bdaddr(tg, _TAG_BTCTL)
        if bdaddr is not None:
            print(f"MMP bdaddr: {bdaddr}",flush=True)
        else:
            print("No MMP detected",flush=True)

        gc.collect()

        print("Waiting for processes to exit")
        await tg.sp_terminate(_TAG_BTCTL)
        await tg.wait_for_processes()

    # The await is implicit when the context manager exits.
    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(mmp_main())
