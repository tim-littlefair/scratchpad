#! python3

import json
import re
import sys

class SharkJsonParser :

    def __init__(self,filenames):
        self.frames = []
        for fn in filenames:
            print(f"# Parsing {fn}")
            self.frames += json.load(open(fn))


    @staticmethod
    def _frame_attr(frame, pdpkl):
        # pdpkl stands for 'pipe delimited path key list'
        key_list = list(reversed(list(pdpkl.split("|"))))
        target = frame
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
            f"{item_key}:{
                # TODO: Replace empty strings only with ""
                # re.replace(
                str(node.get(node_key_prefix+item_key,None))
                # ,'^$',.'""')
            }"
            for item_key
            in subkey_list
        ]
        return ",".join(loggable_values)


    @staticmethod
    def process_command_frame(frame, frame_number):
        bthci_cmd = SharkJsonParser._frame_attr(frame, "_source|layers|bthci_cmd")
        if bthci_cmd is None:
            return False
        opcode = bthci_cmd['bthci_cmd.opcode']
        ogf = 0x003F&(int(opcode,16)>>10)
        ocf = 0x03FF&int(opcode,16)
        param = bthci_cmd['bthci_cmd.param_length']
        param += ": " + str(bthci_cmd.get('bthci_cmd.parameter',None))
        print(f"# Frame: {frame_number} command {ogf:03x}:{ocf:04x} {param}")
        return True

    @staticmethod
    def process_attribute_frame(frame, frame_number):
        btatt = SharkJsonParser._frame_attr(frame, "_source|layers|btatt")
        if btatt is None:
            return False
        opcode = btatt['btatt.opcode']
        handle = btatt.get('btatt.handle',None)
        value = btatt.get('btatt.value',None)
        print(f"# Frame: {frame_number} attribute {opcode} {handle} {value}")
        return True

    @staticmethod
    def process_event_frame(frame, frame_number):
        bthci_evt = SharkJsonParser._frame_attr(frame, "_source|layers|bthci_evt")
        if bthci_evt is None:
            return False
        loggable_subkeys = "code|param_length|le_meta_subevent|le_features|bd_addr|data_length|status|command_in_frame"
        print(
            f"# Frame: {frame_number} event {
                SharkJsonParser._node_parameter_string(
                    bthci_evt,"bthci_evt.", loggable_subkeys
                )
            }"
        )
        return True


    @staticmethod
    def process_acl_frame(frame, frame_number):
        bthci_acl = SharkJsonParser._frame_attr(frame, "_source|layers|bthci_acl")
        if bthci_acl is None:
            return False
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
    print(f"# Message count: {len(sjp.frames)}")
    for frame in sjp.frames:
        print()
        frame_number = int(SharkJsonParser._frame_attr(frame, '_source|layers|frame|frame.number'))
        if SharkJsonParser.process_command_frame(frame, frame_number):
            SharkJsonParser.process_acl_frame(frame, frame_number)
            pass
        elif SharkJsonParser.process_attribute_frame(frame, frame_number):
            SharkJsonParser.process_acl_frame(frame, frame_number)
            pass
        elif SharkJsonParser.process_event_frame(frame, frame_number):
            SharkJsonParser.process_acl_frame(frame, frame_number)
            pass
        elif SharkJsonParser.process_acl_frame(frame, frame_number):
            pass
        else:
            print("# frame not handled")
