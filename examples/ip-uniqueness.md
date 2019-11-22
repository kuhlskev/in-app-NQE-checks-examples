## Find duplicate IP addresses within a VRF

***Name:*** Interface IP  
***Intent:*** unique within a single VRF  
***Description:*** This check finds instances of IP addresses that are assigned to multiple interfaces within a single VRF.
The check iterates over devices and VRFs to get the VRF's interfaces, and then looks up the referenced interfaces to
get IP addresses on the VRF interfaces. Then, the check groups the data by the combination of VRF and IP address,
with each group containing the locations at which the vrf and IP were found. The query then filters to those groups
that have multiple locations. Finally, the diagnosis includes, for each VRF+IP combination that is located at
multiple interfaces, the count of locations at which it was defined, as well as a comma-separated list of locations.  

***Query:***
```
foreach device in network.devices
foreach vrf in device.networkInstances
foreach ifaceSubiface in vrf.interfaces
foreach iface in device.interfaces
foreach subIface in iface.subinterfaces
where iface.name == ifaceSubiface.ifaceName &&
      subIface.name == ifaceSubiface.subIfaceName
foreach address in subIface.ipv4.addresses
let location = { device: device.name, iface: iface.name }
group location as locations by { vrf: vrf.name,
                                 ip: address.ip
                               } as vrfIp
where length(locations) > 1
select { vrf: vrfIp.vrf,
         ip: vrfIp.ip,
         count: length(locations),
         locations: (foreach loc in locations
                     select loc.device + ":" + loc.iface)
       }
```

***Notes:***
The expression ***loc.device + ":" + loc.iface*** in the select expression joins the device name, colon, and iface name (since these three expressions are all strings).

***Query result example:***
![In-App NQE Checks Interface Unique IP](/images/in-app-nqe-checks-example-ip-uniqueness.png?width=800px&classes=shadow)
