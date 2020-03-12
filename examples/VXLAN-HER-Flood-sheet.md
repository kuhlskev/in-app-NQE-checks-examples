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
