import asyncio
import binascii
import sys
import time
import traceback

from signal import SIGINT
from asyncio.subprocess import PIPE, STDOUT

async def _check_process(tag, proc, timeout=0.1, timeout_count=None):
    try:
        async with asyncio.timeout(0.1):
            err = (await proc.stderr.read()).decode().strip()
            if len(err)>0:
                print(f"{tag} error:\n{err}", flush=True)
            out = (await proc.stdout.read()).decode().strip()
            if len(out)>0:
                print(f"{tag} output:\n{out}")
            if proc.returncode is not None:
                print(f"{tag} returned {proc.returncode}", flush=True)
            if timeout_count is not None:
                print(f"{tag} processed after {timeout_count} timeouts", flush=True)
                timeout_count = 0
    except asyncio.exceptions.CancelledError:
        print(f"{tag} processing cancelled", flush=True)
    except asyncio.exceptions.TimeoutError:
        if timeout_count is not None:
            timeout_count += 1
        else :
            print(f"{tag} timed out", flush=True)
    return timeout_count

async def run_commands(bdaddr, commands):
    hd_proc = False
    for c in commands:
        c = c.strip()
        if c.startswith("#"):
            # commented out command
            continue
        if hd_proc is None:
            hd_proc = await asyncio.create_subprocess_shell(
                "btmon",
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
            )
        if len(c)==0:
            continue
        print(f"processing command '{c}'")
        if c.startswith("!sleep"):
            sleep_length_seconds = float(c.replace("!sleep","").strip())
            print(f"sleeping for {sleep_length_seconds}s ... ",end="", flush=True)
            await asyncio.sleep(sleep_length_seconds)
            print("awake")
            continue
        else:
            ht_proc = await asyncio.create_subprocess_shell(
                f"hcitool {c}",
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE
            )
            await ht_proc.wait()
            await _check_process("hcitool",ht_proc)

        if hd_proc is None or hd_proc is False:
            pass
        elif hd_proc.returncode is None:
            hd_proc.send_signal(9)
            await hd_proc.wait()
            await _check_process("hcidump", hd_proc)
            hd_proc = None
        else:
            await _check_process("hcidump", hd_proc)
            hd_proc = None



async def main(args):
    async with bleak.BleakScanner() as scanner:
        print("Scanning...")
        bd, ad, client = await find_ble_device(scanner, args)
        print(f"{bd!r} with {ad!r}")
        print("Connected")
        try:
            await client.connect()
            # await client.pair()
        except:
            traceback.print_exc(2)
        handle_db = await get_handles(client)
        await probe_characteristics(client, handle_db)
        await asyncio.sleep(10.0)
        print("Exiting")

if __name__ == "__main__":
    bdaddr = sys.argv[1]
    bdaddr_arg_string = " ".join(
        reversed(list([f"0x{bd_byte_hex}" for bd_byte_hex in bdaddr.split(":") ]))
    )
    print(bdaddr_arg_string)
    commands = f"""
        # 3x vendor-specific command
        # Probably not needed
        # cmd 0x3f 0x0157 0x00 0x00 0x00
        # cmd 0x3f 0x0157 0x00 0x00 0x00
        # cmd 0x3f 0x0157 0x00 0x00 0x00

        # LE scan disable
        cmd 0x08 0x000c 0x00 0x01

        # set LE scan parameters
        cmd 0x08 0x000b 0x01 0x80 0x00 0x32 0x00 0x01 0x00

        # LE scan
        cmd 0x08 0x000c    0x01 0x00
        !sleep 2

        # LE connect???
        cmd 0x08 0x000d    0x00 0x30   0x00 0x60   0x00   0x00   {bdaddr_arg_string}   0x01  0x00 0x18   0x00 0x28   0x00 0x00   0x01 0xf4   0x00 0x00   0x00 0x00

        # LE scan disable
        cmd 0x08 0x000c    0x00 0x01

        # Wait for connection to complete
        !sleep 10

        # Read remote features
        # parameter is connection handle - for Android FenderTone always 2, not sure where it needs to come from
        cmd 0x08 0x0016    0x00 0x02
        !sleep 10


    """.split("\n")
    asyncio.run(run_commands(bdaddr, commands))
