import asyncio
import binascii
import sys
import traceback

import bleak
import bleak.args

def disconnect_cb(client):
    print(f"Disconnecting {client}")


async def find_ble_device(scanner, args):
    async for bd, ad in scanner.advertisement_data():
        if ad.local_name not in args:
            pass
        else:
            try:
                print(ad)
                if len(ad.service_uuids)==0:
                    await asyncio.sleep(1.0)
                    return
                client = bleak.BleakClient(
                    bd, disconnect_cb,
                    # pair=True,
                )
                return bd, ad, client
            except:
                traceback.print_exc(2)
                pass

def notify_cb(sender, data):
    print(f"notify_cb {sender}: {data}")

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
        handle_db = {}
        services = client.services
        services_found = 0
        remaining_attempts = 3
        while services_found == 0 and remaining_attempts > 0:
            for s in services:
                services_found += 1
                handle_db[s.handle]=("S",s)
                for c in s.characteristics:
                    handle_db[c.handle]=("C",c)
                    for d in c.descriptors:
                        handle_db[d.handle]=("D",d)
            if services_found == 0:
                try:
                    print("Trying to get services")
                    services = await client._backend._get_services()
                    print("Services retrieved", services)
                except:
                    traceback.print_exc(1)
                    services_found = -1
            await asyncio.sleep(1)
            remaining_attempts -= 1
        for h in sorted(handle_db.keys()):
            print(f"{h:04x} {h:04d}: {handle_db[h][0]} {handle_db[h][1]}")
        print("Services, Characteristics and Descriptors listed")
        ccc_uuid = bleak.uuids.normalize_uuid_16(0x2902)
        cfs_uuid = bleak.uuids.normalize_uuid_16(0x2b29)
        for h in sorted(handle_db.keys()):
            record_type, record_value = handle_db[h]
            if record_type == "C":
                try:
                    if record_value.uuid == cfs_uuid:
                        cfs_value = await client.read_gatt_char(record_value)
                        print(f"CFS characteristic {record_value.uuid} has value {binascii.b2a_hex(cfs_value)}")

                    else:
                        #char_value = await client.read_gatt_char(record_value)
                        #print(f"characteristic {record_value.uuid} has value {binascii.b2a_hex(char_value)}")
                        await client.start_notify(
                            record_value, notify_cb,
                            bluez=bleak.args.bluez.BlueZNotifyArgs(use_start_notify = True)
                        )
                        print(f"Notify enabled on {h}")
                except bleak.exc.BleakError as e:
                    print(str(e))
                    if 'NotSupported' in str(e):
                        pass
                    elif 'READ_NOT_PERMITTED' in str(e):
                        pass
                    else:
                        print(str(e))
                        traceback.print_exc(1)
                        pass
            if record_value.uuid in (ccc_uuid):
                assert record_type == "D"
                ccc_value = await client.read_gatt_descriptor(h)
                print(f"descriptor {record_value.uuid[4:8]} for characteristic {record_value.characteristic_uuid} has value {binascii.b2a_hex(ccc_value)}")
        print("CCC's dumped")
        await asyncio.sleep(10.0)
        print("Exiting")


if __name__ == "__main__":
    asyncio.run(main(sys.argv))
