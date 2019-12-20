# In-App Network Query Engine (NQE) Checks

Network Query Engine (NQE) by Forward Networks provides information about the network as JSON data in a fully-parsed form.
The information is normalized and presented uniformly across devices from different vendors.
The exported data structures are standards-aligned with [OpenConfig](http://www.openconfig.net/) (details below), and all data is available through a [GraphQL](https://github.com/forwardnetworks/network-query-engine#graphql-interface) API as well as custom verification checks directly in the Forward Enterprise browser-based interface ([In-App NQE Checks](#in-app-nqe-checks)).

This repository helps you get started with the In-App NQE Checks.

Please check out this [blog post](https://www.forwardnetworks.com/blog/network-query-engine) for more information on NQE and this [GitHub repo](https://github.com/forwardnetworks/network-query-engine-examples) for some examples based on the GraphQL API.  

<a id="in-app-nqe-checks"></a>
## Getting Started

As stated above, ***In-App NQE Checks*** augments NQE by enabling IT teams to create custom verification checks using the NQE data model, directly in the Forward Enterprise browser-based interface.

Following you can find a screenshot from the Forward Enterprise GUI with a simple query to find every interface whose admin status is UP but operational status is not UP.

![In-App NQE Checks example](/images/in-app-nqe-checks-example.png?width=800px&classes=shadow)

Moreover, In-App NQE Checks, allows to build custom verification checks even for device configuration and state data that is not fully parsed and normalized by providing an easy way to match patterns in the configuration files.
This new capability is very important for use cases like vendor specific information or for data that is not published on NQE [yet].
Check the [In-App Device Config Checks Examples](#device-config-checks-examples) section for some examples.

In-App NQE Checks can be saved in the Forward Enterprise platforms and verified every time a new network collection is taken, as with any other Verification Check.

<a id="in-app-nqe-checks-examples"></a>
## In-App NQE Checks Examples
In this section you can find some examples based on fully parsed and normalized NQE data.

  * [Find every interface whose admin status is UP but operational status is not UP](/examples/interface-status.md)
  * [Find IPv4 summary routes that are not in a specific allowed list](/examples/summary-routes.md)
  * [Find loopback interfaces assigned subnets bigger than /32](/examples/loopback-subnet.md)
  * [Find connected interfaces that have mismatched MTU settings](/examples/mtu-mismatch.md)
  * [Find duplicate IP addresses within a VRF](/examples/ip-uniqueness.md)
  * [Find all devices no running latest certified software](/examples/certified-software.md)
  * [Find interface with no description, except loopbacks](/examples/interface-description.md)

<a id="device-config-checks-examples"></a>
## In-App Device Config Checks Examples

In this section you can find some examples based on **no** fully parsed and normalized data from device configuration files.

  * [Find disallowed enabled features on Cisco NX-OS devices](/examples/nxos-disallowed-features.md)
  * [Find all static null routes on Cisco NX-OS devices](/examples/nxos-null-static-routes.md)
  * [Find all interface speeds slower than 1Gbps on Cisco NX-OS devices](/examples/nxos-interface-speed.md)

<a id="contribute"></a>
## How to contribute

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

## Contact

[@AndreasVoellmy](@AndreasVoellmy) or use the project GitHub issues.

## Further reading

* [Product docs](https://app.forwardnetworks.com/docs/docs/applications/network_query_engine/)
* [Network Query Engine Blog Post](https://www.forwardnetworks.com/blog/network-query-engine)
* [Network Query Engine main repository](https://github.com/forwardnetworks/network-query-engines)
* [Network Query Engine examples based on GraphQL](https://github.com/forwardnetworks/network-query-engine-examples)
