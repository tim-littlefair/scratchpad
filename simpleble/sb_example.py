import asyncio
import sys

#from simplepyble.aio import Adapter
from simplepyble import Adapter

async def main():
    adapters = Adapter.get_adapters()
    adapter = adapters[0]
    target_device = None

    adapter.scan_for(5000)
    peripherals = adapter.scan_get_results()
    for peripheral in peripherals:
        print(f"Found: {peripheral.identifier()} [{peripheral.address()}]")
    target_device = [ p for p in peripherals if p.identifier() in sys.argv ][0]
    print(f"Target: {target_device!r}")

    target_device.connect()
    await asyncio.sleep(10)
    print("Successfully connected, listing services...")

    if True:
        # """
        services = target_device.services()
        service_characteristic_pair = []
        for service in services:
            for characteristic in service.characteristics():
                service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

        if not service_characteristic_pair:
            print("No services or characteristics found.")
            return
        # """





if __name__ == "__main__":
    asyncio.run(main())
