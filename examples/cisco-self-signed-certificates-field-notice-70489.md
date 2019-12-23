## Cisco Field Notice: FN - 70489 - PKI Self-Signed Certificate Expiration in Cisco IOS and Cisco IOS XE Software

***Name:*** Cisco FN#70489 - IOS-PKI Self-Signed Certificate Expiration  

***Intent:*** Find Cisco device affected by the Field Notice 70489  

***Description:*** This check finds all Cisco device running IOS and Cisco IOS XE software affected by the [Field Notice 70489](https://www.cisco.com/c/en/us/support/docs/field-notices/704/fn70489.html)  
Problem description:  
Self-signed X.509 PKI certificates (SSC) that were generated on devices that run affected Cisco IOS or Cisco IOS XE software releases expire on 2020-01-01 00:00:00 UTC. New self-signed certificates cannot be created on affected devices after 2020-01-01 00:00:00 UTC. Any service that relies on these self-signed certificates to establish or terminate a secure connection might not work after the certificate expires.

Check the Field Notice for workarounds and solutions.

***Query:***
```
affectedVersions =
  ["12.*",
   "15.0.*",
   "15.1.*",
   "15.2.*",
   "15.3.*",
   "15.4.*",
   "15.5.*",
   "15.6(1)S",
   "15.6(1)S1",
   "15.6(1)S2",
   "15.6(1)S3",
   "15.6(1)S4",
   "15.6(1)SN",
   "15.6(1)SN1",
   "15.6(1)T",
   "15.6(1)T0a",
   "15.6(1)T1",
   "15.6(1)T2",
   "15.6(1)T3",
   "15.6(2)S",
   "15.6(2)S1",
   "15.6(2)S2",
   "15.6(2)S3",
   "15.6(2)S4",
   "15.6(2)SP",
   "15.6(2)SP1",
   "15.6(2)SP2",
   "15.6(2)SP3",
   "15.6(2)SP4",
   "15.6(2)SP6",
   "15.6(2)T",
   "15.6(2)T0a",
   "15.6(2)T1",
   "15.6(2)T2",
   "15.6(2)T3",
   "15.6(3)M",
   "15.6(3)M0a",
   "15.6(3)M1",
   "15.6(3)M1a",
   "15.6(3)M1b",
   "15.6(3)M2",
   "15.6(3)M2a",
   "15.6(3)M3",
   "15.6(3)M3a",
   "15.6(3)M4",
   "15.6(3)M5",
   "15.6(3)M6",
   "15.6(3)M6a",
   "15.7(3)M",
   "15.7(3)M1",
   "15.7(3)M2",
   "15.7(3)M3",
   "15.7(3)M4",
   "15.7(3)M4a",
   "15.7(3)M4b",
   "15.8(3)M",
   "15.8(3)M0a",
   "15.8(3)M0b",
   "15.8(3)M1",
   "15.8(3)M1a",
   "15.8(3)M2",
   "15.8(3)M2a",
   "15.9(3)M0a",
   "16.1.0",
   "16.1.1",
   "16.1.2",
   "16.1.3",
   "16.2.1",
   "16.2.2",
   "16.3.1",
   "16.3.1a",
   "16.3.2",
   "16.3.3",
   "16.3.4",
   "16.3.5",
   "16.3.5b",
   "16.3.6",
   "16.3.7",
   "16.3.8",
   "16.3.9",
   "16.4.1",
   "16.4.2",
   "16.4.3",
   "16.5.1",
   "16.5.1a",
   "16.5.1b",
   "16.5.2",
   "16.5.3",
   "16.6.1",
   "16.6.1a",
   "16.6.2",
   "16.6.3",
   "16.6.4",
   "16.6.4a",
   "16.6.5",
   "16.6.5a",
   "16.6.6",
   "16.6.7",
   "16.7.1",
   "16.7.1a",
   "16.7.1b",
   "16.7.2",
   "16.7.3",
   "16.7.4",
   "16.8.1",
   "16.8.1a",
   "16.8.1b",
   "16.8.1c",
   "16.8.1d",
   "16.8.1e",
   "16.8.2",
   "16.8.3"
  ];


isAffectedPlatform(device) =
  (device.platform.os == OS.IOS || device.platform.os == OS.IOS_XE) &&
  (!isPresent(device.platform.osVersion) || length((foreach versionPattern in affectedVersions
                                                    where matches(device.platform.osVersion, versionPattern)
                                                    select versionPattern)) > 0);

getTrustPointsWithSelfSignedCerts(d) =
  foreach line in d.files.config
  let crypto = patternMatch(line.text, `crypto pki trustpoint {tpName:string}`)
  where isPresent(crypto)
  let enrollmentLines = (foreach cryptoLine in line.children
                         where isPresent(patternMatch(cryptoLine.text, `enrollment selfsigned`))
                         select cryptoLine.text)
  where length(enrollmentLines) > 0
  let certLines = (foreach line in d.files.config
                   let cryptoCertChain = patternMatch(line.text, `crypto pki certificate chain {tpName:string}`)
                   where isPresent(cryptoCertChain) && cryptoCertChain.tpName == crypto.tpName
                   foreach certLine in line.children
                   where isPresent(patternMatch(certLine.text, `certificate self-signed`))
                   select certLine.text)
  select { tpName: crypto.tpName,
           numSelfSignedCerts: length(certLines)
         };

usedInHttpSecureServer(line) =
  isPresent(patternMatch(line.text, `ip http secure-server`));

usedInHttpSecureTrustpoint(line, tpName) =
  length((foreach match in [patternMatch(line.text, `ip http secure-trustpoint {tpName:string}`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select line)) > 0;

usedInSipOverTls(line, tpName) =
  length((foreach match in [patternMatch(line.text, `crypto signaling default trustpoint {tpName:string}`),
                            patternMatch(line.text, `crypto signaling remote-addr {ipv4Address} {ipv4Address} trustpoint {tpName:string}`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select line)) > 0;

usedInTelephonyService(line, tpName) =
  isPresent(patternMatch(line.text, `telephony-service`)) &&
  length((foreach child in line.children
          let match1 = patternMatch(child.text, `secure-signaling trustpoint {tpName:string}`)
          let match2 = patternMatch(child.text, `tftp-server-credentials trustpoint {tpName:string}`)
          where isPresent(match1) &&
                match1.tpName == tpName || isPresent(match2) &&
                match2.tpName == tpName
          select child.text)) > 0;

usedInCredentials(line, tpName) =
  isPresent(patternMatch(line.text, `credentials`)) &&
  length((foreach child in line.children
          let match = patternMatch(child.text, `trustpoint {tpName:string}`)
          where isPresent(match) && match.tpName == tpName
          select child.text)) > 0;

usedInDspFarm(line, tpName) =
  isPresent(patternMatch(line.text, `dspfarm profile {number} {"conference" | "mtp" | "transcode"} security`)) &&
  length((foreach match in [patternMatch(line.text, `trustpoint {tpName:string}`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select match)) > 0;

usedInStcApp(line, tpName) =
  length((foreach match in [patternMatch(line.text, `stcapp security trustpoint {tpName:string}`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select match)) > 0;

usedInWebVpn(line, tpName) =
  isPresent(patternMatch(line.text, `webvpn gateway {string}`)) &&
  length((foreach match in [patternMatch(line.text, `ssl trustpoint {tpName:string}`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select match)) > 0;

usedInSslVpn(line, tpName) =
  isPresent(patternMatch(line.text, `crypto ssl policy {string}`)) &&
  length((foreach match in [patternMatch(line.text, `pki trustpoint {tpName:string} sign`)
                           ]
          where isPresent(match) && match.tpName == tpName
          select match)) > 0;

usedInIkeV2(line, tpName) =
  isPresent(patternMatch(line.text, `crypto ikev2 profile {string}`)) &&
  length((foreach subline in line.children
          where isPresent(patternMatch(subline.text, `authentication local rsa-sig`))
          select line.text)) > 0 &&
  length((foreach subline in line.children
          let match = patternMatch(subline.text, `pki trustpoint {tpName:string}`)
          where isPresent(match) && match.tpName == tpName
          select line.text)) > 0;

usedInIsaKmpProfile(line, tpName) =
  isPresent(patternMatch(line.text, `crypto isakmp profile {string}`)) &&
  length((foreach subline in line.children
          let match = patternMatch(subline.text, `ca trustpoint {tpName:string}`)
          where isPresent(match) && match.tpName == tpName
          select line.text)) > 0;

usedInIsaKmpPolicy(line, tpName) =
  isPresent(patternMatch(line.text, `crypto isakmp policy {number}`)) &&
  length((foreach subline in line.children
          let match = patternMatch(subline.text, `authentication {method:string}`)
          where isPresent(match) &&
                match.method not in ["pre-share",
                                     "rsa-encr"
                                    ]
          select line.text)) > 0;

usedInIsaKmp(line, tpName) =
  usedInIsaKmpProfile(line, tpName) || usedInIsaKmpPolicy(line, tpName);

usedInSshServer(line, tpName) =
  isPresent(patternMatch(line.text, `ip ssh server certificate profile`)) &&
  length((foreach subline in line.children
          where isPresent(patternMatch(subline.text, `server`))
          foreach subsubline in subline.children
          let match = patternMatch(subsubline.text, `trustpoint sign {tpName:string}`)
          where isPresent(match) && match.tpName == tpName
          select line.text)) > 0;

usedInRestConf(line, tpName) =
  isPresent(patternMatch(line.text, `restconf`)) &&
  length((foreach subline in line.children
          let match = patternMatch(subline.text, `ip http {"client" | empty} secure-trustpoint {tpName:string}`)
          where isPresent(match) && match.tpName == tpName
          select line.text)) > 0;

trustpointFeatures(device, tpName) =
  foreach line in device.files.config
  where usedInHttpSecureServer(line) ||
        usedInHttpSecureTrustpoint(line, tpName) ||
        usedInSipOverTls(line, tpName) ||
        usedInTelephonyService(line, tpName) ||
        usedInCredentials(line, tpName) ||
        usedInDspFarm(line, tpName) ||
        usedInStcApp(line, tpName) ||
        usedInWebVpn(line, tpName) ||
        usedInSslVpn(line, tpName) ||
        usedInSshServer(line, tpName) ||
        usedInRestConf(line, tpName) ||
        usedInIkeV2(line, tpName) ||
        usedInIsaKmp(line, tpName)
  select line.text;

foreach device in network.devices
where isAffectedPlatform(device)
foreach tp in getTrustPointsWithSelfSignedCerts(device)
let features = trustpointFeatures(device, tp.tpName)
where length(features) > 0
select { Confidence: if tp.numSelfSignedCerts > 0 then "High" else "Medium",
         Device: device.name,
         OS: device.platform.os,
         Version: device.platform.osVersion,
         TrustPointName: tp.tpName,
         Features: features
       }
```

***Query result example:***
![Cisco Field Notice 70489](/images/in-app-nqe-checks-example-cisco-field-notice-70489.png?width=800px&classes=shadow)

***Notes:***
By default Forward Enterprise filters out sensitive data (e.g., password fields, SNMP server names) from the device configuration.
The check provides a **Confidence** level based on the data collected.
To get more accurate check results, you need to disable the data filtering in the Collector configuration Advanced settings.

![Disable Data Filtering](/images/disable-data-filtering.png?width=800px&classes=shadow)
