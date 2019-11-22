## Find all static null routes on Cisco NX-OS devices

***Name:*** NX-OS static routes  
***Intent:*** no null routes on NX-OS  
***Description:*** This query illustrates that text matching patterns may include components such as ***ipv4Subnet*** that match specific types of entities, not just strings.  

***Query:***
```
foreach device in network.devices
where device.platform.vendor == Vendor.CISCO &&
      device.platform.os == OS.NXOS
foreach line in device.files.config
let match = patternMatch(line.text, `ip route {prefix:ipv4Subnet} Null0`)
where isPresent(match)
select { device: device.name, prefix: match.prefix }
```

***Query result example:***
![In-App NQE Checks null Static Routes](/images/in-app-nqe-checks-example-nxos-null-static-routes.png?width=800px&classes=shadow)
