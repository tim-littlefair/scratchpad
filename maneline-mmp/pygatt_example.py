import pygatt
from binascii import hexlify
import sys
import time
import traceback

import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value),flush=True)

try:
    adapter.start()
    device = adapter.connect(sys.argv[1], timeout=12)

    #for uuid in device.discover_characteristics().keys():
    #    print("Read UUID %s: %s" % (uuid, hexlify(device.char_read(uuid))))

    for uuid_arg in sys.argv[2:]:
        op_in_progress = None
        try:
            if len(uuid_arg)==4:
                uuid_arg=f"0000{uuid_arg}-0000-1000-8000-00805f9b34fb"
            op_in_progress = "subscribing to "
            device.subscribe(uuid_arg,callback=handle_data)
            print("subscribe completed")
        except:
            print(f"Exception while {op_in_progress} {uuid_arg}:")
            traceback.print_exc()

    # The subscription runs on a background thread. You must stop this main
    # thread from exiting, otherwise you will not receive any messages, and
    # the program will exit. Sleeping in a while loop like this is a simple
    # solution that won't eat up unnecessary CPU, but there are many other
    # ways to handle this in more complicated program. Multi-threaded
    # programming is outside the scope of this README.
    countdown = 30
    while countdown>0:
        time.sleep(1)
        countdown-=1
        print(f"\rCountdown: {countdown:2d}\r",end="",flush=True)

finally:
    adapter.stop()
