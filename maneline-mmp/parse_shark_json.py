#! python3

import json
import sys

class SharkJsonParser :

    def __init__(self,filenames):
        self.messages = []
        for fn in filenames:
            print(f"Parsing {fn}")
            self.messages += json.load(open(fn))


if __name__ == "__main__":
    sjp = SharkJsonParser(sys.argv[1:])
    print(len(sjp.messages))
