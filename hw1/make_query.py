import subprocess
import sys

args = sys.argv
assert(len(args) == 1, 'Bad number of args, must be one')

subprocess.run(["curl", "-XGET", "http://localhost:2000/get_result?method=" + args[0].lower()])