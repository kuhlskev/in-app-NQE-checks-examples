import json
import requests
from pprint import PrettyPrinter
pp = pprint.PrettyPrinter(indent=4)

limit= 10000
offset = 0
snapshot = 304634
base64auth = 'your base64 auth combo of user and apikey'

nqe = '''foreach device in network.devices
foreach line in device.files.config
foreach child in line.children
let match = patternMatch(child.text, `vxlan vlan {vlan:string} flood vtep {ips:(string*)}`)
where isPresent(match)
select {
  deviceName: device.name,
  line: child.text,
  vlan: match.vlan,
  ip: match.ips
}'''

url = "https://fwd.app/api/snapshots/%s/nq" % (snapshot)
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic %s' %(base64auth)}
payload = '{"query": "% s","queryOptions":{"offset": %s,"limit": %s }}' % (nqe, offset, limit)
payload = payload.replace('\n', '\\n')
response = requests.request("POST", url, headers=headers, data = payload).json()
pp.pprint (response)
