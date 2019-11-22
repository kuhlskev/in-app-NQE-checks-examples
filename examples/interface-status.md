## Find every interface whose admin status is UP but operational status is not UP

***Name:*** Interface Status  
***Intent:*** Admin up -> Oper up  
***Description:*** This check iterates through all interfaces on all devices and returns the device name and interface name for each qualified interface.

***Query:***
```
    foreach device in network.devices
    foreach interface in device.interfaces
    where interface.adminStatus == AdminStatus.UP &&
          interface.operStatus != OperStatus.UP
    select {
      deviceName: device.name,
      interfaceName: interface.name,
      adminStatus: interface.adminStatus,
      operStatus: interface.operStatus
    }
```
***Notes:***
Please refer to the ***Data Model*** tab for possible values for ***AdminStatus*** and ***OperStatus***.

***Query result example:***
![In-App NQE Checks Interface Status](/images/in-app-nqe-checks-example-interface-status.png?width=800px&classes=shadow)
