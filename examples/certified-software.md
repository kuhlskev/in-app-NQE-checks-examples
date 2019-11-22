## Find all devices no running latest certified software

***Name:*** Certified Software  
***Intent:*** All devices should be running certified software only  
***Description:*** This checks looks for network   devices no running the latest certified software from different network vendors.

***Query:***
```
foreach device in network.devices
let platform = device.platform
where isPresent(platform.osVersion) &&
      (platform.vendor == Vendor.CISCO && platform.osVersion != "9.2(4)" ||
       platform.vendor == Vendor.JUNIPER && platform.osVersion != "14.1R5.4" ||
       platform.vendor == Vendor.ARISTA && platform.osVersion != "4.15.0F" ||
       platform.vendor == Vendor.VMWARE && platform.osVersion != "6.5.0")
select { vendor: platform.vendor,
         os: platform.os,
         deviceName: device.name,
         osVersion: platform.osVersion
       }
```

***Query result example:***
![In-App NQE Checks Certified Software](/images/in-app-nqe-checks-example-certified-software.png?width=800px&classes=shadow)
