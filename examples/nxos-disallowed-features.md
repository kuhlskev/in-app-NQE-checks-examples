## Find disallowed enabled features on Cisco NX-OS devices

***Name:*** NX-OS features  
***Intent:*** disallowed features are not configured on NX-OS  
***Description:*** This query locates instances of the ***feature*** config line in NXOS devices and extracts the named feature from these config lines.
It checks the enabled features against a set of features that ***should not*** be enabled.  

***Query:***
```
disallowedFeatures = ["telnet", "scp-server"];

foreach device in network.devices
where device.platform.vendor == Vendor.CISCO &&
      device.platform.os == OS.NXOS
foreach line in device.files.config
let match = patternMatch(line.text, `feature {featureName:string}`)
where isPresent(match) &&
      match.featureName in disallowedFeatures
select { Device: device.name,
         Feature: match.featureName,
         Fix: "no feature " + match.featureName
       }
```

***Query result example:***
![In-App NQE Checks NX-OS features](/images/in-app-nqe-checks-example-nxos-disallowed-features.png?width=800px&classes=shadow)
