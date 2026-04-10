import asyncio
import sys

from bleak import BleakScanner, BleakClient

def disconnect_cb(client):
    print(f"Disconnecting {client}")


async def find_ble_device(scanner, args):
    async for bd, ad in scanner.advertisement_data():
        if ad.local_name not in args:
            pass
        else:
            client = BleakClient(
                bd, disconnect_cb,
                pair=True,
            )
            return bd, ad, client


async def main(args):
    async with BleakScanner() as scanner:
        print("Scanning...")
        bd, ad, client = await find_ble_device(scanner, args)
        print(f"{bd!r} with {ad!r}")
        await client.connect()
        print("Connected")
        handle_db = {}
        for s in client.services:
            handle_db[s.handle]=("S",s)
            for c in s.characteristics:
                handle_db[c.handle]=("C",c)
                for d in c.descriptors:
                    handle_db[d.handle]=("D",d)
        for h in sorted(handle_db.keys()):
            print(f"{h:04x} {h:04d}: {handle_db[h][0]} {handle_db[h][1]}")
        print("Services, Characteristics and Descriptors listed")


if __name__ == "__main__":
    asyncio.run(main(sys.argv))
