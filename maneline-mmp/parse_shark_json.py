#! python3

import json
import sys

class SharkJsonParser :

    def __init__(self,filenames):
        self.messages = []
        for fn in filenames:
            print(f"Parsing {fn}")
            self.messages += json.load(open(fn))


    @staticmethod
    def message_attr(message, pdkl):
        # pdkl stands for 'pipe delimited key list'
        key_list = list(reversed(list(pdkl.split("|"))))
        target = message
        while len(key_list)>0:
            key = key_list.pop()
            # print(key, key_list)
            if key not in target:
                return None
            elif len(key_list)==0:
                return target[key]
            else:
                target = target[key]

    @staticmethod
    def process_command_message(message):
        bthci_cmd = SharkJsonParser.message_attr(message, "_source|layers|bthci_cmd")
        if bthci_cmd is None:
            return False
        frame_number = int(SharkJsonParser.message_attr(message, '_source|layers|frame|frame.number'))
        opcode = bthci_cmd['bthci_cmd.opcode']
        param = bthci_cmd['bthci_cmd.param_length']
        param += ": " + bthci_cmd.get('bthci_cmd.parameter',"-")
        print(f"# Frame: {frame_number} command {opcode} {param}")
        return True

    @staticmethod
    def process_attribute_message(message):
        btatt = SharkJsonParser.message_attr(message, "_source|layers|btatt")
        if btatt is None:
            return False
        frame_number = int(SharkJsonParser.message_attr(message, '_source|layers|frame|frame.number'))
        opcode = btatt['btatt.opcode']
        handle = btatt.get('btatt.handle','-')
        value = btatt.get('btatt.value','-')
        print(f"# Frame: {frame_number} attribute {opcode} {handle} {value}")
        return True

    @staticmethod
    def process_event_message(message):
        bthci_evt = SharkJsonParser.message_attr(message, "_source|layers|bthci_evt")
        if bthci_evt is None:
            return False
        frame_number = int(SharkJsonParser.message_attr(message, '_source|layers|frame|frame.number'))
        event_code = bthci_evt['bthci_evt.code']
        print(f"# Frame: {frame_number} event code {event_code}")
        return True


if __name__ == "__main__":
    sjp = SharkJsonParser(sys.argv[1:])
    print(len(sjp.messages))
    for m in sjp.messages:
        if SharkJsonParser.process_command_message(m):
            pass
        elif SharkJsonParser.process_attribute_message(m):
            pass
        elif SharkJsonParser.process_event_message(m):
            pass
        else:
            pass
