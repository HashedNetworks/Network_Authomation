import requests
import json
from pprint import pprint
from getpass import getpass

from urllib3.exceptions import InsecureRequestWarning
import ipdb

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

if __name__ == "__main__":

   # ipdb.set_trace()
    http_headers = {"Content-Type": "application/jason-rpc;"}
    host = "192.168.1.124"
    port = "80"
    username = "agarcia"
    password = "cisco123"

    url = "http://{}:{}/command-api".format(host, port)

    json_payload = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {"version": 1,
         "cmds": ["show version",
                   "show ip arp",
                   "show ip route",
                   "show ip interface brief"
         ],
         "format": "json"},
        "id": "1",
    }

    json_data = json.dumps(json_payload)


    http_headers["Content-length"] = str(len(json_data))


    response = requests.post(
        url,
        headers = http_headers,
        auth = (username, password),
        data = json_data,
        #verify = False,
    )

    response = response.json()
    #pprint(response)
    pprint(response["result"][3])


    # print()
    # pprint(response)
    # print()

