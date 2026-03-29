#! python3

import json
import sys

class SharkJsonParser :

    def __init__(self,filenames):
        self.messages = []
        for fn in filenames:
            print(f"# Parsing {fn}")
            self.messages += json.load(open(fn))


    @staticmethod
    def _message_attr(message, pdpkl):
        # pdpkl stands for 'pipe delimited path key list'
        key_list = list(reversed(list(pdpkl.split("|"))))
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
    def _node_parameter_string(node,node_key_prefix,pdskl,):
        # pdpkl stands for 'pipe delimited sub-key list'
        subkey_list = list(pdskl.split("|"))
        loggable_values = [
            f"{item_key}:{str(node.get(node_key_prefix+item_key,None))}"
            for item_key
            in subkey_list
        ]
        return ",".join(loggable_values)


    @staticmethod
    def process_command_message(message):
        bthci_cmd = SharkJsonParser._message_attr(message, "_source|layers|bthci_cmd")
        if bthci_cmd is None:
            return False
        frame_number = int(SharkJsonParser._message_attr(message, '_source|layers|frame|frame.number'))
        opcode = bthci_cmd['bthci_cmd.opcode']
        ogf = 0x003F&(int(opcode,16)>>10)
        ocf = 0x03FF&int(opcode,16)
        param = bthci_cmd['bthci_cmd.param_length']
        param += ": " + str(bthci_cmd.get('bthci_cmd.parameter',None))
        print(f"# Frame: {frame_number} command {opcode} {ogf:03x} {ocf:03x} {param}")
        return True

    @staticmethod
    def process_attribute_message(message):
        btatt = SharkJsonParser._message_attr(message, "_source|layers|btatt")
        if btatt is None:
            return False
        frame_number = int(SharkJsonParser._message_attr(message, '_source|layers|frame|frame.number'))
        opcode = btatt['btatt.opcode']
        handle = btatt.get('btatt.handle',None)
        value = btatt.get('btatt.value',None)
        print(f"# Frame: {frame_number} attribute {opcode} {handle} {value}")
        return True

    @staticmethod
    def process_event_message(message):
        bthci_evt = SharkJsonParser._message_attr(message, "_source|layers|bthci_evt")
        if bthci_evt is None:
            return False
        frame_number = int(SharkJsonParser._message_attr(message, '_source|layers|frame|frame.number'))
        loggable_subkeys = "code|le_features|command_in_frame"
        print(
            f"# Frame: {frame_number} event {
                SharkJsonParser._node_parameter_string(bthci_evt,"bthci_evt.", loggable_subkeys)
            }"
        )
        return True

    @staticmethod
    def process_acl_message(message):
        bthci_acl = SharkJsonParser._message_attr(message, "_source|layers|bthci_acl")
        if bthci_acl is None:
            return False
        frame_number = int(SharkJsonParser._message_attr(message, '_source|layers|frame|frame.number'))
        loggable_names = "chandle|pb_flag|bc_flag|length|data|mode|src.name".split("|")
        loggable_values = [
            f"{item_key}:{bthci_acl[".".join(["bthci_acl",item_key])]}"
            for item_key
            in loggable_names
        ]
        print(f"# Frame: {frame_number} acl: {','.join(loggable_values)}")
        return True


if __name__ == "__main__":
    sjp = SharkJsonParser(sys.argv[1:])
    print(f"# Message count: {len(sjp.messages)}")
    for m in sjp.messages:
        print()
        if SharkJsonParser.process_command_message(m):
            SharkJsonParser.process_acl_message(m)
            pass
        elif SharkJsonParser.process_attribute_message(m):
            SharkJsonParser.process_acl_message(m)
            pass
        elif SharkJsonParser.process_event_message(m):
            SharkJsonParser.process_acl_message(m)
            pass
        elif SharkJsonParser.process_acl_message(m):
            pass
        else:
            print("# message not handled")
