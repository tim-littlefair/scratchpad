import asyncio
from simplepyble.aio import Adapter

async def main():
    adapters = Adapter.get_adapters()
    adapter = adapters[0]

    async with adapter:
        await adapter.scan_for(5000)
        peripherals = adapter.scan_get_results()
        for peripheral in peripherals:
            print(f"Found: {peripheral.identifier()} [{peripheral.address()}]")

if __name__ == "__main__":
    asyncio.run(main())
