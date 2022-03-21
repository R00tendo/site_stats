import sys
import requests
import fnmatch
import warnings
import time
import hashlib
warnings.simplefilter("ignore")
class readconf:
    class arguments:
        None


    class options:
         valid = "-u -w".split(' ')


    def __init__(self, args):
        for arg in args:
             if arg not in self.options.valid and sys.argv[sys.argv.index(arg) -1] not in self.options.valid:
                 print(f"Argument {arg} is invalid!")
             elif sys.argv[sys.argv.index(arg) -1] in self.options.valid:
                 setattr(self.arguments, arg, True)


class response:
     None


remo_useless = dir(readconf.arguments)
args2 = readconf(sys.argv[1::]).arguments
args = args2
args = set(dir(args))
args = args.symmetric_difference(remo_useless)

if len(args) != len(readconf.options.valid):
   print("Too much or too little arguments, arguments are: -u <url>, -w <write stats to>")
   sys.exit(1)
if len(sys.argv) < len(readconf.options.valid) +3:
   print("You didn't provide the values for the parameters like this: -u https://example.com -w site.stats")
   sys.exit(1)

url = sys.argv[sys.argv.index("-u") +1]
write = sys.argv[sys.argv.index("-w") +1]
print(f"Requesting:{url}")

try:
  start = time.time()
  resp = requests.get(url, verify=False, allow_redirects=False, timeout=10)
  end = time.time() - start
except requests.exceptions.ConnectionError:
  print("Site not responsive!") 
  sys.exit(1)

response.status_code = resp.status_code
response.hash = hashlib.md5(bytes(resp.text, "utf-8")).hexdigest()
response.headers = resp.headers
response.time = end

print(f"Writing to:{write}") 


file_open = open(write, "wb")

stat_format = f"""STATUS CODE: {response.status_code}

SITES MD5 HASH: {response.hash}

TIME FOR (FULL HTML LOAD): {response.time}
"""

stat_format = bytes(stat_format, "utf-8")
file_open.write(stat_format)
file_open.close()
print("ALL DONE!")
sys.exit(0)



