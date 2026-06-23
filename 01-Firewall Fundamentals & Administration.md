# Firewall Fundamentals

Understanding firewall technologies, traffic filtering, firewall types, Next-Generation Firewalls (NGFWs), and common firewall evasion techniques from a SOC analyst perspective.

## Introduction

Firewalls are a critical component of network security. They monitor, inspect, and filter traffic between trusted and untrusted networks based on predefined security policies. Modern firewalls can also provide advanced capabilities such as intrusion prevention, application awareness, and encrypted traffic inspection.


<img width="1536" height="1024" alt="ChatGPT Image 23 Haz 2026 22_05_22" src="https://github.com/user-attachments/assets/0211927f-1430-4224-bf15-778967603e34" />

> Conceptual overview of how modern firewalls inspect, filter, and control network traffic while allowing legitimate communication and blocking malicious activity.

After completing my SIEM Investigation Case Studies project, I wanted to expand my knowledge into another essential area of cybersecurity: firewall technologies and network security.

Firewalls play a critical role in protecting modern networks by monitoring and controlling incoming and outgoing traffic based on predefined security rules. Acting as a security barrier between trusted internal networks and untrusted external sources, they help prevent unauthorized access, block malicious activity, and enforce organizational security policies.

For SOC analysts, understanding how firewalls operate is fundamental. Firewall logs often provide valuable evidence during security investigations, helping analysts identify suspicious connections, detect scanning activity, investigate potential attacks, and understand network communication patterns.

In this module, I will explore the fundamental concepts of firewall technology, different firewall types, firewall rules, and the role firewalls play in network defense. I will also examine how firewall data can support security monitoring and incident investigations in real-world environments.

By building a strong foundation in firewall technologies, security analysts can better understand network activity and improve their ability to detect and respond to potential threats.

## Types of Firewalls

<img width="1536" height="1024" alt="ChatGPT Image 23 Haz 2026 22_15_32" src="https://github.com/user-attachments/assets/306c288f-8d21-438e-87af-552114549238" />

> Comparison of firewall technologies, inspection methods, OSI layer coverage, and security capabilities used to protect modern networks.

### Stateless Firewall

Stateless firewalls operate primarily at OSI layers 3 and 4 and evaluate each packet independently against predefined rules. They do not maintain information about previous connections, making them fast and efficient but less capable of applying context-aware security decisions.

### Stateful Firewall

Stateful firewalls monitor active connections and maintain a state table containing information about ongoing sessions. By understanding the context of network traffic, they can make more intelligent filtering decisions and provide stronger security than stateless firewalls.

### Proxy Firewall

Proxy firewalls act as intermediaries between internal users and external resources. Operating at the application layer, they inspect packet contents, hide internal IP addresses, and provide advanced content filtering capabilities.

### Next-Generation Firewall (NGFW)

NGFWs combine traditional firewall functionality with advanced security features such as deep packet inspection, intrusion prevention, application awareness, SSL/TLS inspection, and threat intelligence integration. They are widely used in modern enterprise environments.

| Firewall Type | Key Characteristics |
|--------------|--------------------|
| Stateless | Fast packet filtering, no connection tracking |
| Stateful | Tracks active sessions and connection states |
| Proxy | Inspects application-layer traffic and content |
| NGFW | Deep packet inspection, IPS, application awareness |

## Why Firewalls Matter for SOC Analysts

Firewalls are one of the most important sources of network visibility in modern environments. During security investigations, firewall logs can help analysts identify suspicious connections, detect scanning activity, investigate command-and-control communication, and monitor potential data exfiltration attempts.

Understanding how firewalls operate and how they generate logs enables SOC analysts to perform more effective investigations and respond to security incidents with greater confidence.

## Firewall Rule Components

Every firewall rule is built using several key elements that determine how traffic is handled.

- **Source Address** – The IP address originating the traffic.
- **Destination Address** – The target IP address receiving the traffic.
- **Port** – The network port used for communication.
- **Protocol** – The communication protocol, such as TCP or UDP.
- **Action** – The decision applied to the traffic (Allow, Deny, or Forward).
- **Direction** – Whether the rule applies to inbound or outbound traffic.

  ## Directionality of Rules

Firewall rules can be categorized based on the direction of the network traffic they control. Understanding traffic direction is important when creating security policies and investigating network activity.

### Inbound Rules

Inbound rules apply to traffic entering a device or network. These rules are commonly used to allow or restrict access to services such as web servers, file servers, or remote administration interfaces.

### Outbound Rules

Outbound rules apply to traffic leaving a device or network. Organizations often use outbound filtering to prevent unauthorized communications, restrict applications, and reduce the risk of data exfiltration.

### Forward Rules

Forward rules are used to redirect traffic to another host or network segment. This functionality is commonly used when publishing internal services or forwarding external requests to internal systems.

## Types of Firewall Actions

### Allow

The Allow action permits traffic that matches a firewall rule and enables legitimate communication between systems.

### Deny

The Deny action blocks traffic that matches a firewall rule and prevents the connection from being established.

### Forward

The Forward action redirects traffic to another host or network segment based on the configured firewall policy.

## Windows Defender Firewall

Windows Defender Firewall is the built-in host-based firewall solution included with Microsoft Windows. It allows administrators to create inbound and outbound rules, monitor network traffic, and control access to system resources.

In this section, I explored the Windows Defender Firewall interface and reviewed how firewall rules can be configured to manage network communications.

The Windows Defender Firewall dashboard provides an overview of active network profiles and firewall settings. From this interface, administrators can manage inbound and outbound traffic, adjust security policies, and access advanced firewall configuration options.


<img width="1121" height="586" alt="Ekran görüntüsü 2026-06-16 215816" src="https://github.com/user-attachments/assets/bd90a197-a697-466e-b300-3fa41cbe9b31" />

> Windows Defender Firewall dashboard displaying available network profiles and firewall management options.


## Firewall Classification by Deployment

Firewalls can also be classified based on how they are deployed within an environment.

### Hardware Firewall

Hardware firewalls are dedicated network appliances positioned between networks. They inspect traffic before it reaches internal systems and are commonly used in enterprise environments.

Examples include:

- Cisco ASA
- Fortinet FortiGate
- Palo Alto Networks
- WatchGuard Firebox

### Software Firewall

Software firewalls run directly on operating systems and provide host-based protection.

Examples include:

- Windows Defender Firewall
- Linux iptables
- Linux firewalld

Software firewalls allow organizations to enforce security policies at the individual host level.

---

## Packet Filtering Firewall

Packet-filtering firewalls are the most basic type of firewall technology.

They inspect:

- Source IP Address
- Destination IP Address
- Protocol
- Source Port
- Destination Port

Each packet is evaluated independently against predefined firewall rules. Because no connection state information is stored, packet-filtering firewalls are considered stateless firewalls.

While they provide fast performance, they cannot understand the context of a network session.

---

## How Firewalls Inspect Network Traffic

Firewalls make filtering decisions by inspecting specific fields within network packets. Depending on the firewall type, these fields may include information from the IP header, TCP/UDP header, or even the application layer.

At a minimum, most firewalls inspect:

- Protocol (TCP, UDP, ICMP)
- Source IP Address
- Destination IP Address
- Source Port
- Destination Port

These fields allow administrators to create security policies that permit or block specific network communications.

---

## Protocol-Based Filtering

Traditional packet-filtering firewalls evaluate traffic based on network protocols and addressing information.

Common protocols inspected by firewalls include:

- TCP (Transmission Control Protocol)
- UDP (User Datagram Protocol)
- ICMP (Internet Control Message Protocol)

By filtering traffic according to protocol type, organizations can restrict unnecessary network communications and reduce the attack surface.

---

## Port-Based Filtering

Many firewall rules rely on TCP and UDP port numbers to identify services.

| Service | Default Port |
| ------- | ------------ |
| HTTP    | 80           |
| HTTPS   | 443          |
| DNS     | 53           |
| SSH     | 22           |
| RDP     | 3389         |

Although port-based filtering remains effective, modern applications may use non-standard ports. As a result, advanced firewalls often perform deeper traffic inspection rather than relying solely on port numbers.

---

## Firewall Inspection Across OSI Layers

Different firewall technologies operate at different layers of the OSI model.

| Firewall Type                   | OSI Layers        |
| ------------------------------- | ----------------- |
| Packet Filtering                | Layer 3 - Layer 4 |
| Stateful Firewall               | Layer 3 - Layer 4 |
| Proxy Firewall                  | Layer 7           |
| Next-Generation Firewall (NGFW) | Layer 3 - Layer 7 |

As firewall technologies become more advanced, they gain visibility into higher network layers and can inspect application-level traffic, user activity, and encrypted communications.

---

## Key Takeaways for SOC Analysts

Throughout this project, I explored how firewalls inspect network traffic, enforce security policies, and generate valuable security telemetry.

Key concepts covered include:

- Firewall architectures
- Stateful and stateless inspection
- Protocol and port-based filtering
- Firewall rule components
- Traffic direction and actions
- Host-based firewall management

Understanding firewall behavior is essential for SOC analysts because firewall logs frequently provide evidence of reconnaissance activity, unauthorized access attempts, malware communications, and potential data exfiltration.

Firewall visibility plays a critical role in incident investigations, threat hunting activities, and overall network security monitoring.

## Firewall Evasion Techniques

During network reconnaissance and penetration testing activities, attackers may attempt to bypass firewall filtering and security monitoring controls. Nmap provides several techniques that can alter packet characteristics, disguise scan origins, and reduce the likelihood of detection by traditional security devices.

Common techniques include decoy scanning, IP and MAC address spoofing, source port manipulation, packet fragmentation, and port tunneling. Understanding these methods helps security analysts recognize suspicious network behavior and investigate potential firewall evasion attempts.

<img width="1536" height="1024" alt="ChatGPT Image 23 Haz 2026 22_19_49" src="https://github.com/user-attachments/assets/e9aca6c7-238f-4971-876b-dff0aa9fab9e" />

> Firewall evasion techniques may appear during reconnaissance, penetration testing, or malicious activity. Understanding these methods helps security analysts detect suspicious network behavior and investigate potential security incidents.

### Decoy Scanning

Nmap allows the use of decoy IP addresses during a scan to disguise the true source of reconnaissance activity.

Example:

nmap -sS -Pn -D RND,RND,ME -F TARGET_IP

This technique generates traffic that appears to originate from multiple source IP addresses, making attribution more difficult during network monitoring.


### Source Port Manipulation

Some firewalls apply filtering decisions based on source port numbers. Nmap can modify the source port used during scanning.

Example:

nmap -sS -Pn -g 8080 -F TARGET_IP

Using a trusted source port may help bypass poorly configured firewall rules that rely only on port-based filtering.

### IP Address Spoofing

IP spoofing alters the source IP address contained in packets to disguise the origin of network traffic.

Example:

nmap -sS -Pn -S SPOOFED_IP TARGET_IP

This technique can be used to obscure scan origins or exploit trust relationships between systems.

### MAC Address Spoofing

Attackers can modify their MAC address to impersonate another device on the local network.

Example:

nmap --spoof-mac MAC_ADDRESS TARGET_IP

MAC spoofing may help evade simple network access controls that rely on MAC address identification.


### Packet Fragmentation

Packet fragmentation breaks network traffic into smaller fragments, potentially reducing visibility to legacy filtering devices.

Common options include:

- `-f` → Fragment packets into 8-byte chunks
- `-ff` → Fragment packets into 16-byte chunks
- `--mtu` → Specify a custom MTU value
- `--data-length` → Append random data to packets

Modern IDS/IPS and Next-Generation Firewalls typically reassemble fragmented packets before inspection, reducing the effectiveness of this technique.


### Key Takeaway

Understanding firewall evasion techniques helps SOC analysts recognize suspicious network behavior and identify reconnaissance activities that may otherwise appear as normal traffic. While modern security solutions can detect many of these methods, awareness of these techniques remains important during investigations and threat hunting activities.



### SOC Analyst Perspective

During investigations, analysts may encounter fragmented packets, unusual MTU values, or packets containing unexpected amounts of padding data. These characteristics can indicate reconnaissance activity, firewall evasion attempts, or penetration testing operations.

Modern IDS/IPS and Next-Generation Firewalls typically reassemble fragmented packets before inspection, reducing the effectiveness of these techniques. However, analysts should remain aware of them when reviewing network traffic.

### Port Tunneling

Port tunneling is a technique that forwards network traffic from one port to another port that is allowed through a firewall.

For example, if a firewall blocks traffic to TCP port 80 but allows TCP port 8080 or 443, traffic can be redirected through the permitted port and forwarded internally to the blocked service.

This technique is commonly used by attackers to bypass network filtering controls and maintain communication with internal services.

### Lab Demonstration

In this lab, Ncat was used to create a simple port forwarding tunnel. Traffic received on TCP port 8008 was forwarded to an internal web service running on TCP port 80.

<img width="802" height="159" alt="Ekran görüntüsü 2026-06-23 214139" src="https://github.com/user-attachments/assets/bab4891e-6d7d-46db-b68a-d0a4909a050a" />

> Ncat was used to create a simple port forwarding tunnel between TCP ports 8008 and 80. This demonstrates how traffic can be redirected through an allowed port to reach an internal service that would otherwise be inaccessible due to firewall restrictions.

### SOC Analyst Perspective

Security analysts should monitor for unusual port forwarding activity and unexpected communication patterns between services. Port tunneling may indicate attempts to bypass firewall restrictions, hide malicious traffic, or access internal systems through alternative communication channels.

## Next-Generation Firewalls (NGFW)

<img width="1536" height="1024" alt="ChatGPT Image 23 Haz 2026 22_42_10" src="https://github.com/user-attachments/assets/c1221a13-54ad-4f28-a067-22310ad29afc" />

> Overview of Next-Generation Firewall (NGFW) capabilities, including deep packet inspection, application awareness, intrusion prevention, SSL/TLS inspection, threat intelligence, and advanced traffic visibility.


Traditional firewalls primarily rely on IP addresses, ports, and protocols to make filtering decisions. However, modern applications often use encryption and non-standard ports, making traditional filtering less effective.

Next-Generation Firewalls (NGFWs) provide advanced security capabilities beyond basic packet filtering, including:

* Integrated Intrusion Prevention System (IPS)
* Application Awareness and Control
* User and Identity Awareness
* Deep Packet Inspection (DPI)
* Content Inspection
* SSL/TLS Traffic Inspection

By inspecting traffic at the application layer (OSI Layer 7), NGFWs can identify applications, users, and malicious content regardless of the port being used.

### SOC Analyst Perspective

NGFWs provide greater visibility into network traffic and user activity. Security analysts can leverage NGFW logs to detect suspicious applications, policy violations, encrypted threats, and attempts to bypass traditional firewall controls. Properly configured NGFWs significantly improve an organization's ability to detect and prevent modern cyberattacks.


## Firewall Logging & Monitoring

Firewalls generate logs that provide visibility into network traffic, connection attempts, blocked communications, and policy violations.

Common events monitored by security analysts include:

- Allowed and denied connections
- Port scanning activity
- Suspicious outbound traffic
- Firewall rule violations
- Communication with known malicious IP addresses

Firewall logs are commonly integrated into SIEM platforms such as Splunk and Elastic Security to support threat hunting, incident detection, and forensic investigations.

> Firewall logs often provide valuable evidence during security investigations and help analysts identify suspicious network behavior.


## Conclusion

This project explored the fundamental concepts of firewall technologies, traffic filtering mechanisms, firewall rule management, and common firewall evasion techniques.

In addition to traditional firewall architectures, I examined advanced security capabilities provided by Next-Generation Firewalls (NGFWs), including deep packet inspection, application awareness, intrusion prevention, and SSL/TLS inspection.

I also explored how firewall logs support security monitoring, threat hunting, and incident investigations within modern SOC environments.

Understanding how firewalls inspect, filter, and log network traffic is an essential skill for security analysts, as firewall telemetry often provides critical evidence during cybersecurity investigations and incident response activities.





















