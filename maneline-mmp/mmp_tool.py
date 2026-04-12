import asyncio
import binascii
import sys
import traceback

from bleak_helper import main

if __name__ == "__main__":
    asyncio.run(main(["Mustang Micro Plus"]))
