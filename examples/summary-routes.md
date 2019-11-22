## Find IPv4 summary routes that are not in a specific allowed list

***Name:*** v4 summary routes  
***Intent:*** in allowed list  
***Description:*** This check iterates through all IPv4 routes on all devices and returns those routes whose prefix length is less than 8 and whose prefix is not in a specific allowed list of summary subnets.  

***Query:***
```
foreach device in network.devices
foreach vrf in device.networkInstances
where isPresent(vrf.afts.ipv4Unicast)
foreach ipEntry in vrf.afts.ipv4Unicast.ipEntries
where length(ipEntry.prefix) <= 8
let allowedSummarySubnets = [ipSubnet("224.0.0.0/4"),  ipSubnet("117.0.0.0/8")]
where ipEntry.prefix not in allowedSummarySubnets
select {
  device: device.name,
  vrf: vrf.name,
  prefix: ipEntry.prefix
}
```

***Notes:***
The ***length*** function works on both lists and IP subnets, as in this example.

***Query result example:***
![In-App NQE Checks Summary Routes](/images/in-app-nqe-checks-example-summary-routes.png?width=800px&classes=shadow)
