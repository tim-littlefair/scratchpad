# Examples based on  https://docs.python.org/3/library/asyncio-task.html

import asyncio
import collections
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
    async def sp_read(self,tag, silence_timeout=1.0):
        p = self.subprocess_map[tag]
        if silence_timeout is None:
            silence_timeout = p.timeout_factor
        retval = bytes()
        read_again = True
        while read_again is True:
            try:
                async with asyncio.timeout(silence_timeout):
                    next_chunk = await p.stdout.read(1)
                    retval += next_chunk
            except TimeoutError:
                read_again = False
        if p.text_io:
            retval = retval.decode()
        return retval
    async def sp_terminate(self, tag, timeout=None):
        if tag not in self.subprocess_map:
            print(f"{tag} was not started")
            return
        p = self.subprocess_map[tag]
        if p.returncode is not None:
            print(f"{tag} has already exited")
            return
        if timeout is None:
            timeout = p.timeout_factor
        # Different processes might require different signals to exit.
        # We try the in this order:
        # SIGTERM=15 (canonical polite request for process to end)
        # SIGHUP=1   (simulates closure of input FD)
        # SIGINT=2   (simulates ctrl-C on input)
        # SIGQUIT=3  (simulates break on input)
        # SIGKILL=9  (canonical mandatory process end signal)
        for termination_signal in ( 15, 1, 2, 3, 9 ):
            async with asyncio.timeout(p.timeout_factor*2):
                try:
                    print(f"Sending signal {termination_signal}")
                    p.send_signal(termination_signal)
                    await asyncio.sleep(p.timeout_factor)
                    await p.wait()
                    break
                except TimeoutError:
                    print(f"{tag} communication timed out")
                except asyncio.exceptions.CancelledError:
                    print(f"{tag} read cancelled")
        status = await p.wait()
        # We expect the status to be equal to the negation of the last signal sent
        print(f"{tag} has exited with status {status}")
        # Violating the privacy of p._transport to ensure that it is
        # manually closed before garbage collection runs is a workaround for
        # uncatchable exceptions generated on exit described in
        # https://github.com/python/cpython/issues/114177
        p._transport.close()

    async def wait_for_processes(self, timeout_factor=None):
        while len(self.subprocess_map)>0:
            k = list(self.subprocess_map.keys())[0]
            print(f"Stopping process {k}",flush=True)
            p = self.subprocess_map[k]
            assert p.returncode is not None
            so, se = await p.communicate()
            if p.text_io:
                so = so.decode()
            print(f"trailing output from {k}:\n{so}\n")
            assert se is None
            del self.subprocess_map[k]
            # del self.task_map[k]
        return

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


async def get_mmp_bdaddr(task_group, btctl_tag, hdmp_tag):
    await asyncio.sleep(1.0)
    await task_group.sp_write(btctl_tag,"\n") # for output clarity
    await task_group.sp_write(btctl_tag,"scan.transport le\n")
    await task_group.sp_write(btctl_tag,"scan.clear\n")
    await task_group.sp_write(btctl_tag,"scan.pattern 'Mustang Micro Plus'\n")
    await task_group.sp_write(btctl_tag,"scan on\n")
    bd_addr = None
    for _ in range(0,3):
        await asyncio.sleep(2.0)
        scan_output = await task_group.sp_read(btctl_tag,2.0)
        print(scan_output)
        bdaddr_pattern = re.compile(r"Device ([:\d\w]+) RSSI")
        bdaddr_match = bdaddr_pattern.search(scan_output)
        if bdaddr_match is not None:
            bd_addr = bdaddr_match.group(1)
            break
    await task_group.sp_write(btctl_tag,"scan off\n")
    try:
        output = await task_group.sp_read(btctl_tag,2.0)
        print(output)
    except asyncio.exceptions.CancelledError:
        pass
    return bd_addr

async def subscribe_for_gatt_replies(task_group, tag, bdaddr):
    await asyncio.sleep(0.1)
    await task_group.sp_write(tag,"\n") # for output clarity
    await task_group.sp_write(tag,f"connect {bdaddr}\n")
    await asyncio.sleep(1.0)
    await task_group.sp_write(tag,f"gatt.list-attributes\n")
    await asyncio.sleep(1.0)
    char_output=await task_group.sp_read(tag,1.0)
    print(f"Connect output:\n>>>>\n{char_output}\n<<<<\n")
    read_notify_char_pattern = re.compile(r"(/org/bluez/\w+/\w+/service0015/char0016)")
    read_notify_char_match = read_notify_char_pattern.search(char_output)
    if read_notify_char_match is None:
        raise RuntimeError("Failed to find GATT characteristic for HOGP read/notify")
    read_notify_bluez_path = read_notify_char_match.group(1)
    write_char_pattern = re.compile(r"(/org/bluez/\w+/\w+/service0015/char001a)")
    write_char_match = write_char_pattern.search(char_output)
    if write_char_match is None:
        raise RuntimeError("Failed to find GATT characteristic for HOGP write")
    write_bluez_path = write_char_match.group(1)
    return ( read_notify_bluez_path, write_bluez_path )

async def mmp_main():
    _TAG_BTCTL = "btctl"
    _TAG_HDMPRAW = "hdmp-raw"
    _TAG_HDMPCKD = "hdmp-cooked"
    print(f"started at {time.strftime('%X')}")
    async with SubprocessTaskGroup() as tg:

        try:
            btctl_task = await tg.create_subprocess_task(_TAG_BTCTL,"bluetoothctl --timeout 2")
            bdaddr = await get_mmp_bdaddr(tg, _TAG_BTCTL, _TAG_HDMPRAW)
            if bdaddr is not None:
                print(f"MMP bdaddr: {bdaddr}",flush=True)
            else:
                raise RuntimeError("No MMP detected")

            ( read_notify_bluez_path, write_bluez_path)  = await subscribe_for_gatt_replies(tg, _TAG_BTCTL, bdaddr)

            hcidump_task1 = await tg.create_subprocess_task(_TAG_HDMPRAW,"hcidump --raw")
            hcidump_task2 = await tg.create_subprocess_task(_TAG_HDMPCKD,"hcidump -X")
            await tg.sp_write(_TAG_BTCTL, f"gatt.select-attribute {read_notify_bluez_path}\n")
            await tg.sp_write(_TAG_BTCTL, f"gatt.notify on\n")
            print(f"Subscribed for HOGP responses on {read_notify_bluez_path}")
            await tg.sp_write(_TAG_BTCTL, f"gatt.select-attribute {write_bluez_path}\n")
            print(f"Sending HOGP commands and requests to {write_bluez_path}")

            # await tg.sp_read(_TAG_HDMPRAW,1.0)
            # await tg.sp_read(_TAG_HDMPCKD,1.0)
            for msg in (
                # "--char-write --handle=0x0018 --value=0x0100",
                # "'0x35 0x00 0x02 0x1a 0x00' 0 0",
                # "--char-write --handle=0x001b --value=0x3500040a023a00",
                # "--char-write --handle=0x001b --value=0x3500040a027200",
                # "--char-write --handle=0x001b --value=0x3500060a0422020801",
                # "--char-write --handle=0x001b --value=0x3500050a03ca0100",
                # "--char-write-req --handle=0x001b --value=0x3500041a020801",
                # "--char-read --handle=0x0017"
            ):
                await tg.sp_write(_TAG_BTCTL, f"gatt.write {msg}\n")
                print(await tg.sp_read(_TAG_BTCTL, 3.0))
                print(await tg.sp_read(_TAG_HDMPRAW,1.0))
                print(await tg.sp_read(_TAG_HDMPCKD,1.0))


        except RuntimeError:
            traceback.print_exception(sys.exc_info()[1])

        finally:
            await tg.sp_write(_TAG_BTCTL,"quit\n")

        # Drain unread hcidump output
        # await tg.sp_read(_TAG_HDMPRAW,1.0)
        # await tg.sp_read(_TAG_HDMPCKD,1.0)

        print("Terminating processes")
        await tg.sp_terminate(_TAG_BTCTL)
        await tg.sp_terminate(_TAG_HDMPRAW)
        await tg.sp_terminate(_TAG_HDMPCKD)
        print("Waiting for processes to exit")
        await tg.wait_for_processes()

    # The await is implicit when the context manager exits.
    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    try:
        asyncio.run(mmp_main())
    except RuntimeError:
        print("RE in __main__")

