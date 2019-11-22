## Find all interface speeds slower than 1Gbps on Cisco NX-OS devices

***Name:*** NXOS Interface speed  
***Intent:*** all interface configured as 1G or faster  
***Description:*** This check shows how to find information in nested config lines.  

***Query:***
```
foreach device in network.devices
where device.platform.vendor == Vendor.CISCO &&
      device.platform.os == OS.NXOS
foreach line in device.files.config
let ifaceMatch = patternMatch(line.text, `interface {iface:string}`)
where isPresent(ifaceMatch)
foreach childLine in line.children
let speedMatch = patternMatch(childLine.text, `speed {speed:number}`)
where isPresent(speedMatch) && speedMatch.speed < 1000
select { device: device.name,
         iface: ifaceMatch.iface,
         speed: speedMatch.speed
       }
```

***Query result example:***
![In-App NQE Checks Interface Speed](/images/in-app-nqe-checks-example-nxos-interface-speed.png?width=800px&classes=shadow)
