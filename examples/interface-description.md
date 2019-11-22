## Find interface with no description, except loopbacks

***Name:*** Interface Description  
***Intent:*** All interfaces must have a description, except loopbacks  
***Description:*** This checks looks for interfaces with no description except loopbacks.

***Query:***
```
foreach device in network.devices
foreach interface in device.interfaces
where !isPresent(interface.description) && interface.loopbackMode == false
select { deviceName: device.name,
         interfaceName: interface.name,
         description: interface.description,
  		 loopback: interface.loopbackMode
       }
```

***Query result example:***
![In-App NQE Checks Certified Software](/images/in-app-nqe-checks-example-interface-description.png?width=800px&classes=shadow)
