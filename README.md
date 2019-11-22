Table of Content:

  * [NQE and In-App NQE Checks](#chapter-1)  
  * [In-App NQE Checks Examples](#chapter-2)  
  * [In-App Device Config Checks Examples](#chapter-3)  

<a id="chapter-1"></a>
# NQE and In-App NQE Checks
## Network Query Engine (NQE)
***NQE*** is a Forward Networks' enterprise platform (Forward Enterprise) feature that provides to IT teams the ability to query their network details (configurations, links, security rules, routing policies, device status, etc.) like a database.

NQE provides a simple API that exposes information about the network as JSON data in a fully-parsed form. The information is normalized and presented uniformly across devices from different vendors. The exported data structures are standards-aligned with [OpenConfig](http://www.openconfig.net/), and all data is available through a [GraphQL](https://graphql.org/) API. This API allows network operators to easily develop scripts - for example, to perform sanity checks or to display information - that work across the entire fleet of devices in their network.

Please check out this [blog post](https://www.forwardnetworks.com/blog/network-query-engine) for more information on NQE and this [GitHub repo](https://github.com/forwardnetworks/network-query-engine-examples) for some examples.  

## In-App Network Query Engine (NQE) checks

***In-App NQE Checks*** augments NQE by enabling IT teams to create custom verification checks using the NQE data model, directly in the Forward Enterprise browser-based interface.

![In-App NQE Checks example](/images/in-app-nqe-checks-example.png?width=800px&classes=shadow)

In-App NQE Checks can be saved in the Forward Enterprise platforms and verified every time a new network collection is taken.

Moreover, In-App NQE Checks, allows to build custom verification checks even for device configuration and state data that is not fully parsed and normalized by providing an easy way to match patterns in the configuration and state files. Check the [In-App Device Config Checks Examples](#example-6) section for more information and some examples.

<a id="chapter-2"></a>
# In-App NQE Checks Examples
In this section you can find some examples based on fully parsed and normalized NQE data.


  * [Find every interface whose admin status is UP but operational status is not UP](#example-1.1)
  * [Find IPv4 summary routes that are not in a specific allowed list](#example-1.2)
  * [Find loopback interfaces assigned subnets bigger than /32](#example-1.3)
  * [Find connected interfaces that have mismatched MTU settings](#example-1.4)
  * [Find duplicate IP addresses within a VRF](#example-1.5)
  * [Find all devices no running latest certified software](#example-1.6)
  * [Find interface with no description, except loopbacks](#example-1.7)

<a id="example-1.1"></a>
## Find every interface whose admin status is UP but operational status is not UP

The following check iterates through all interfaces on all devices and returns the device name and interface name for each qualified interface.

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

Please refer to the ***Data Model*** tab for possible values for ***AdminStatus*** and ***OperStatus***.

Query result example:
![In-App NQE Checks Interface Status](/images/in-app-nqe-checks-example-interface-status.png?width=800px&classes=shadow)


<a id="example-1.2"></a>
## Find IPv4 summary routes that are not in a specific allowed list

The following check iterates through all IPv4 routes on all devices and returns those routes whose prefix length is less than 8 and whose prefix is not in a specific allowed list of summary subnets.

```
    foreach device in network.devices
    foreach vrf in device.networkInstances
    where isPresent(vrf.afts.ipv4Unicast)
    foreach ipEntry in vrf.afts.ipv4Unicast.ipEntries
    where length(ipEntry.prefix) <= 8
    let allowedSummarySubnets = [ipSubnet("224.0.0.0/4 ipSubnet("117.0.0.0/8")]
    where ipEntry.prefix not in allowedSummarySubnets
    select {
      device: device.name,
      vrf: vrf.name,
      prefix: ipEntry.prefix
    }
```

Note that the ***length*** function works on both lists and IP subnets, as in this example.

Query result example:
![In-App NQE Checks Summary Routes](/images/in-app-nqe-checks-example-summary-routes.png?width=800px&classes=shadow)

<a id="example-1.3"></a>
## Find loopback interfaces assigned subnets bigger than /32

The following check iterates through all subinterfaces and filters the results to return loopback interfaces where the assigned IP subnet is bigger than a /32.

```
    foreach device in network.devices
    foreach iface in device.interfaces
    where iface.loopbackMode
    foreach subIface in iface.subinterfaces
    foreach addr in subIface.ipv4.addresses
    where addr.prefixLength < 32
    select {
      deviceName: device.name,
      ifaceName: iface.name,
      subIfaceName: subIface.name,
      ip: addr.ip,
      prefixLength: addr.prefixLength
    }
```

Query result example:
![In-App NQE Checks Loopback](/images/in-app-nqe-checks-example-loopback.png?width=800px&classes=shadow)

<a id="example-1.4"></a>
## Find connected interfaces that have mismatched MTU settings

The following check iterates through all devices and interfaces, and the links from those interfaces. Then it looks up each connected interface with a second iteration, and then filters to include just those pairs of connected interfaces that have MTU values that are mismatched.

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
    select {
      device1: d1.name,
      iface1: i1.name,
      mtu1: i1.mtu,
      device2: d2.name,
      iface2: i2.name,
      mtu2: i2.mtu
    }
```

Query result example:
![In-App NQE Checks Interface MTU](/images/in-app-nqe-checks-example-mtu.png?width=800px&classes=shadow)

<a id="example-1.5"></a>
## Find duplicate IP addresses within a VRF

The following check finds instances of IP addresses that are assigned to multiple interfaces within a single VRF. The check iterates over devices and VRFs to get the VRF's interfaces, and then looks up the referenced interfaces to get IP addresses on the VRF interfaces. Then, the check groups the data by the combination of VRF and IP address, with each group containing the locations at which the vrf and IP were found. The query then filters to those groups that have multiple locations. Finally, the diagnosis includes, for each multiply defined VRF+IP combination, the count of locations at which it was defined, as well as a comma-separated list of locations.

```
    foreach device in network.devices
    foreach vrf in device.networkInstances
    foreach ifaceSubiface in vrf.interfaces
    foreach iface in device.interfaces
    foreach subIface in iface.subinterfaces
    where iface.name == ifaceSubiface.ifaceName && subIface.name == ifaceSubiface.subIfaceName
    foreach address in subIface.ipv4.addresses
    let location = {device: device.name, iface: iface.name}
    group location as locations by {vrf: vrf.name, ip: address.ip} as vrfIp
    where length(locations) > 1
    select {
      vrf: vrfIp.vrf,
      ip: vrfIp.ip,
      count: length(locations),
      locations: (foreach loc in locations select loc.device + ":" + loc.iface)
    }
```
Note that the expression ***loc.device + ":" + loc.iface*** in the select expression joins the device name, colon, and iface name (since these three expressions are all strings).

Query result example:
![In-App NQE Checks Interface Unique IP](/images/in-app-nqe-checks-example-unique-ip.png?width=800px&classes=shadow)

<a id="example-1.6"></a>
## Find all devices no running latest certified software

The following checks looks for network devices no running the latest certified software from different network vendors.

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

Query result example:
![In-App NQE Checks Certified Software](/images/in-app-nqe-checks-example-certified-software.png?width=800px&classes=shadow)


<a id="example-1.7"></a>
## Find interface with no description, except loopbacks

The following checks looks for interfaces with no description except loopbacks.

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
Query result example:
![In-App NQE Checks Certified Software](/images/in-app-nqe-checks-example-interface-description.png?width=800px&classes=shadow)

<a id="chapter-3"></a>
# In-App device config Checks examples

In this section you can find some examples based on no fully parsed and normalized data from device configuration and state files.

  * [Find not allowed features enabled on Cisco NX-OS devices](#example-2.1)
  * [Find all static null routes on Cisco NX-OS devices](#example-2.2)
  * [Find all interface speeds slower than 1Gbps on Cisco NX-OS devices](#example-2.3)

<a id="example-2.1"></a>
## Find not allowed features enabled on Cisco NX-OS devices
This query locates instances of the feature config line in NX-OS devices and extracts the named feature from these config lines.

```
    foreach device in network.devices
    where device.platform.vendor == Vendor.CISCO &&
          device.platform.os == OS.NXOS
    foreach line in device.files.config
    let match = patternMatch(line.text, `feature {featureName:string}`)
    where isPresent(match)
    select {
        device: device.name,
        feature: match.featureName
    }
```

Query result example:
![In-App NQE Checks NX-OS features](/images/in-app-nqe-checks-example-nxos-features.png?width=800px&classes=shadow)

<a id="example-2.2"></a>
## Find all static null routes on Cisco NX-OS devices
This query illustrates that text matching patterns may include components such as ***ipv4Subnet*** that match specific types of entities, not just strings.

```
    foreach device in network.devices
    where device.platform.vendor == Vendor.CISCO &&
          device.platform.os == OS.NXOS
    foreach line in device.files.config
    let match = patternMatch(line.text, `ip route {prefix:ipv4Subnet} Null0`)
    where isPresent(match)
    select { device: device.name, prefix: match.prefix }
```
Query result example:
![In-App NQE Checks null Static Routes](/images/in-app-nqe-checks-example-null-static-routes.png?width=800px&classes=shadow)

<a id="example-2.3"></a>
## Find all interface speeds slower than 1Gbps on Cisco NX-OS devices
The following query shows how to find information in nested config lines.

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

Query result example:
![In-App NQE Checks Interface Speed](/images/in-app-nqe-checks-example-interface-speed.png?width=800px&classes=shadow)
