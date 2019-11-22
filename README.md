Table of Content:

  * [NQE and In-App NQE Checks](#chapter-1)  
  * [In-App NQE Checks Examples](#chapter-2)  
  * [In-App Device Config Checks Examples](#chapter-3)  
  * [How to contribute](#chapter-4)  

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

  * [Find every interface whose admin status is UP but operational status is not UP](/examples/interface-status.md)
  * [Find IPv4 summary routes that are not in a specific allowed list](/examples/summary-routes.md)
  * [Find loopback interfaces assigned subnets bigger than /32](/examples/loopback-subnet.md)
  * [Find connected interfaces that have mismatched MTU settings](/examples/mtu-mismatch.md)
  * [Find duplicate IP addresses within a VRF](/examples/ip-uniqueness.md)
  * [Find all devices no running latest certified software](/examples/certified-software.md)
  * [Find interface with no description, except loopbacks](/examples/interface-description.md)

<a id="chapter-3"></a>
# In-App device config Checks examples

In this section you can find some examples based on no fully parsed and normalized data from device configuration and state files.

  * [Find disallowed enabled features on Cisco NX-OS devices](/examples/nxos-disallowed-features.md)
  * [Find all static null routes on Cisco NX-OS devices](/examples/nxos-null-static-routes.md)
  * [Find all interface speeds slower than 1Gbps on Cisco NX-OS devices](/examples/nxos-interface-speed.md)

<a id="chapter-4"></a>
# How to contribute

We would love to see new examples from you!!

Your contribution will help other customers and hopefully encourage them to contribute back.

Moreover, you'll get the chance to have your check[s] published to the official Forward Networks documentation with your name as the author :)

Please contribute by:

 * Fork this repository
 * Duplicate the ***template.md*** file in the ***examples*** directory and give it a meaningful name
 * Add a query result screenshot in the ***images*** directory and name it ***in-app-nqe-checks-example-< example title >.png***
 * Update all the info in square brackets in the newly created <example>.md files
 * Add the example to the appropriate table in the ***README.md*** file
 * Send a pull request
 * Wait [for a short time] to hear from us or see it published in this repository

Thanks!!
