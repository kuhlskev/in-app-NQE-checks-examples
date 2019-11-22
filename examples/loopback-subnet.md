## Find loopback interfaces assigned subnets bigger than /32

***Name:*** loopback subnet  
***Intent:*** is a /32  
***Description:*** This check iterates through all subinterfaces and filters the results to return loopback interfaces where the assigned IP subnet is bigger than a /32.  

***Query:***
```
foreach device in network.devices
foreach iface in device.interfaces
where iface.loopbackMode
foreach subIface in iface.subinterfaces
foreach addr in subIface.ipv4.addresses
where addr.prefixLength < 32
select { deviceName: device.name,
         ifaceName: iface.name,
         subIfaceName: subIface.name,
         ip: addr.ip,
         prefixLength: addr.prefixLength
       }
```

***Query result example:***
![In-App NQE Checks Loopback](/images/in-app-nqe-checks-example-loopback-subnet.png?width=800px&classes=shadow)
