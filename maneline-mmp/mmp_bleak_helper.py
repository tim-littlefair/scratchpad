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
        for s in client.services:
            print("S:",s)
            for c in s.characteristics:
                print("C:",c)
                for d in c.descriptors:
                    print("D:",d)
        print("Services, Characteristics and Descriptors listed")


if __name__ == "__main__":
    asyncio.run(main(sys.argv))
