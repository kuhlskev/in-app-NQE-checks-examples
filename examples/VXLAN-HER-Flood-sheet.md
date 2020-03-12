## Find all VXLAN Flood Lists on Arista Switches and return list of Devices, Config Line, Vlans, and associated Flood List

***Name:*** VXLAN Flood List Entries  
***Intent:*** Gather Head End Replication Flood List from All devices  
***Description:*** This checks looks for VXLAN Flood List Entries and returns as list.  

***Query:***
```
foreach device in network.devices
foreach line in device.files.config
foreach child in line.children
let match = patternMatch(child.text, `vxlan vlan {vlan:string} flood vtep {ips:(string*)}`)
where isPresent(match)
foreach ip in match.ips
select {
  deviceName: device.name,
  line: child.text,
  vlan: match.vlan,
  ip: ip
}
```
***Query result example:***
![In-App NQE Checks HER VXLAN List](/images/VXLAN-HER-Flood-sheet.png?width=800px&classes=shadow)
