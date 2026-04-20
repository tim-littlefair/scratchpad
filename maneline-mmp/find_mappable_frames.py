import json
import re
import sys

_MAPPINGS = json.load(open("mappings.json"))

def compile_mappings():
	for item in _MAPPINGS:
		cm = re.compile(item.get("frame_re"))
		item["frame_re"] = cm

def _report_on_invisible_frames(unparsed_count, keepalive_count):
	if unparsed_count + keepalive_count == 0:
		pass
	else:
		print(f"""{
			unparsed_count
		} frames skipped and {
			keepalive_count 
		} keepalive frames since last parsed frame""")

def parse_frames(fn, which_mapping=None):
	frames = json.load(open(fn))
	print(f"Number of frames: {len(frames)}")
	last_parsed_frame = None
	keepalive_count = 0
	unparsed_count = 0
	for f in frames:
		frame_raw = f["_source"]["layers"]["frame_raw"]
		if frame_raw is not None:
			mapping_found = False
			for mapping_item in _MAPPINGS:
				candidate_op_name = mapping_item["frame_op_name"]
				# print(candidate_op_name)
				match = mapping_item["frame_re"].match(frame_raw[0])
				if match is None:
					continue
				elif "KEEPALIVE" in candidate_op_name:
					keepalive_count += 1
					mapping_found = True
					break
				else:
					_report_on_invisible_frames(unparsed_count, keepalive_count)
					frame_number = f["_source"]["layers"]["frame"]["frame.number"]
					print(frame_number, candidate_op_name, match.groups())
					unparsed_count = 0
					keepalive_count = 0
					mapping_found = True
					break
				
			if mapping_found is False:
				unparsed_count += 1			
	_report_on_invisible_frames(unparsed_count, keepalive_count)
				
		
		
	

if __name__ == "__main__":
	compile_mappings()
	parse_frames(sys.argv[1])
	
