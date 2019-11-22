## Find connected interfaces that have mismatched MTU settings

***Name:*** Interface MTU  
***Intent:*** match on interface pair  
***Description:*** The following check iterates through all devices and interfaces, and the links from those interfaces.
Then it looks up each connected interface with a second iteration, and then filters to include just those pairs of connected interfaces that have MTU values that are mismatched.  

***Query:***
```
foreach d1 in network.devices
foreach i1 in d1.interfaces
foreach link in i1.links
foreach d2 in network.devices
where d2.name == link.deviceName
foreach i2 in d2.interfaces
where i2.name == link.ifaceName
where isPresent(i1.mtu) && isPresent(i2.mtu)
where i1.mtu != i2.mtu
select { device1: d1.name,
         iface1: i1.name,
         mtu1: i1.mtu,
         device2: d2.name,
         iface2: i2.name,
         mtu2: i2.mtu
       }
```

***Query result example:***
![In-App NQE Checks Interface MTU](/images/in-app-nqe-checks-example-mtu-mismatch.png?width=800px&classes=shadow)
