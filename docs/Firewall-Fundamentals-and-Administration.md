# Firewall Fundamentals and Administration

## Purpose

I prepared these notes to connect firewall concepts with the questions a SOC analyst asks during an investigation. A firewall can enforce policy and produce useful telemetry, but its logs are only one part of the evidence.

## 1. What a firewall evaluates

A firewall applies policy to network traffic crossing a host or network boundary. Depending on the product, a decision can use:

- Source and destination IP addresses
- Source and destination ports
- Network protocol
- Connection state
- Interface, zone or security profile
- Application, user or device identity
- URL category, threat signature or reputation data

![Overview of firewall traffic control between network zones](https://github.com/user-attachments/assets/0211927f-1430-4224-bf15-778967603e34)

The visible packet fields do not always explain the whole connection. NAT may change addresses, a proxy may create a second connection, and encrypted traffic can limit application inspection. During analysis I therefore record whether a field represents the original client, a translated address or the firewall's observation point.

## 2. Common firewall types

### Stateless packet filtering

A stateless firewall evaluates each packet against a rule set without keeping a connection table. It is fast and simple, but it has less context about whether a packet belongs to a legitimate session.

### Stateful inspection

A stateful firewall tracks active connections. Return traffic can be associated with an existing session instead of being treated as an unrelated packet. State tables are valuable during troubleshooting, but they also have capacity and timeout limits.

### Proxy or application gateway

A proxy terminates a client connection and creates a separate connection to the destination. This can enable application-aware controls and content inspection, while also changing which source address the destination sees.

### Next-generation firewall (NGFW)

NGFW is a product category rather than one fixed feature set. Common capabilities include application identification, identity-aware policy, intrusion prevention, reputation feeds and TLS inspection.

![Comparison of firewall inspection approaches](https://github.com/user-attachments/assets/306c288f-8d21-438e-87af-552114549238)

TLS inspection should not be treated as a simple switch. It requires certificate trust, protected key handling, privacy review, exclusions for sensitive traffic and enough capacity for decryption.

## 3. Rules, actions and evaluation order

A filtering rule normally contains match conditions and an action. Typical filtering actions are **allow**, **block/drop**, **reject** and **log**, although names differ by platform.

Routing, destination NAT and port forwarding affect where traffic goes. They are related to firewall processing, but they are not interchangeable with filtering actions. Keeping these concepts separate makes rule reviews and incident timelines easier to explain.

![Example firewall rule evaluation flow](https://github.com/user-attachments/assets/bd90a197-a697-466e-b300-3fa41cbe9b31)

When reviewing a rule base, I check:

1. Which device and direction see the traffic?
2. Is the policy first-match, last-match or priority based?
3. Is there an established-session rule that applies first?
4. Does NAT occur before or after the filtering decision on this platform?
5. Which rule ID and policy version appear in the log?
6. Is logging enabled for both allowed and blocked activity where needed?

### Rule quality checklist

- Use the narrowest practical source, destination, service and direction.
- Give rules a clear owner and business reason.
- Add an expiry or review date for temporary access.
- Avoid broad rules such as `any` to `any` without a documented reason.
- Review shadowed, duplicate and unused rules.
- Test the expected traffic and a negative case after a change.
- Keep a rollback method before applying the change.

## 4. Host and network firewalls

A network firewall controls traffic at a boundary between segments or security zones. A host firewall applies policy on the endpoint itself. Using both provides different observation points and reduces dependence on one control.

![Host firewall and network firewall deployment example](https://github.com/user-attachments/assets/e9aca6c7-238f-4971-876b-dff0aa9fab9e)

Host firewall logs can identify the local process or profile in some environments. Network firewall logs provide wider visibility across a segment. An analyst should understand which traffic each sensor cannot see, especially with remote users, cloud workloads and east-west traffic.

## 5. Windows Firewall administration

Windows Firewall uses Domain, Private and Public profiles. A rule can apply to one or more profiles, so the active network category matters during troubleshooting.

Useful read-only checks in an elevated PowerShell session include:

```powershell
Get-NetConnectionProfile
Get-NetFirewallProfile |
    Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction

Get-NetFirewallRule -Enabled True |
    Select-Object DisplayName, Direction, Action, Profile
```

Filtering only by display name can be misleading because names are not guaranteed to be unique. For a detailed review I also examine port, address and application filters.

```powershell
$rule = Get-NetFirewallRule -DisplayName "Example rule"
$rule | Get-NetFirewallPortFilter
$rule | Get-NetFirewallAddressFilter
$rule | Get-NetFirewallApplicationFilter
```

The practical exercise in [Windows Firewall Rule Validation Lab](../labs/Windows-Firewall-Rule-Validation.md) creates a narrowly scoped test rule, captures evidence and removes the change.

## 6. Evasion techniques and their limits

Evasion options are useful to study because they reveal weak assumptions in a rule set. They are not guaranteed bypasses. Modern firewalls can normalize, reassemble, correlate or block the traffic.

Only use the following techniques in an isolated lab or an explicitly authorized assessment.

| Technique | Lab example | Important limitation | Defensive question |
| --- | --- | --- | --- |
| Decoy scan | `nmap -sS -Pn -D RND:3,ME -F TARGET_IP` | Can involve unrelated systems and does not hide the real source from every observer | Are many sources probing the same ports within a short window? |
| Chosen source port | `nmap -sS -Pn -g 8080 -F TARGET_IP` | Only helps against poorly designed rules that trust a source port | Do rules trust traffic only because it uses a familiar source port? |
| Spoofed source IP | `nmap -sS -Pn -S LAB_SOURCE_IP TARGET_IP` | Replies normally go to the spoofed address unless the tester controls the route | Do asymmetric paths or impossible internal source addresses appear? |
| Spoofed MAC | `nmap --spoof-mac LAB_MAC TARGET_IP` | Applies to the local Layer 2 segment; routers do not forward the original MAC | Did a known IP suddenly appear with a different MAC on the local segment? |
| IP fragmentation | `nmap -sS -Pn -f TARGET_IP` | Applies to supported raw-packet scan features, not every Nmap function | Does the device reassemble fragments before policy and inspection? |

![Illustration of packet fragmentation during inspection](https://github.com/user-attachments/assets/bab4891e-6d7d-46db-b68a-d0a4909a050a)

Nmap also supports `-ff`, `--mtu` and `--data-length`, but tool behavior and target handling must be verified against the official documentation. I would not interpret a successful scan as proof that a production firewall was bypassed without packet capture and policy evidence.

### Tunnelling and proxying

Tunnelling can carry one protocol through another permitted path. A simple relay can also change the apparent connection path.

![Controlled port relay lab topology](https://github.com/user-attachments/assets/c1221a13-54ad-4f28-a067-22310ad29afc)

An unauthenticated relay must never be exposed to the internet. In a controlled lab, the analyst should compare the connection seen at the client, relay, firewall and destination. Those observations may show different source addresses and process owners.

Defensive indicators can include:

- Long-lived outbound sessions to unusual destinations
- A host receiving connections and immediately opening similar outbound sessions
- Protocol behavior that does not match the expected service port
- Regular beacon-like timing or unusually stable byte ratios
- New listeners or forwarding processes on endpoints

None of these indicators is conclusive by itself.

## 7. Firewall log analysis

### Fields I look for

| Field | Why it matters |
| --- | --- |
| Event time and timezone | Establishes sequence and supports correlation |
| Action | Distinguishes allowed, blocked, rejected and reset traffic |
| Source/destination IP and port | Describes the observed network tuple |
| Direction, interface or zone | Shows the firewall's observation point |
| Protocol and application | Helps compare port use with detected behavior |
| Rule name or rule ID | Connects the event to the effective policy |
| NAT source/destination | Prevents confusion between original and translated addresses |
| Bytes, packets and duration | Helps separate probes from established transfers |
| Device name and policy version | Identifies which control made the decision |

### Triage workflow

1. Normalize timestamps and confirm device clock health.
2. Identify whether the event is inbound, outbound or lateral.
3. Group repeated events into a five- or ten-minute window.
4. Check whether the same activity later changed from denied to allowed.
5. Enrich public IPs and domains, while recording the source and age of enrichment data.
6. Correlate with endpoint process, DNS, proxy, VPN and identity logs.
7. Document alternative explanations and missing evidence.

The [Firewall Detection Notes](../detections/README.md) contains starter SIEM queries for these questions.

## 8. What firewall logs cannot prove alone

- A denied event does not prove that all related traffic was blocked.
- An allowed event does not prove that the activity was malicious.
- A destination port does not always identify the real application.
- Missing logs can be a collection problem rather than absence of activity.
- NAT, proxies and VPNs can change the identity visible at each observation point.

For that reason, my conclusions use confidence levels and name the evidence needed for confirmation.

## References

- [NIST SP 800-41 Rev. 1: Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
- [Microsoft: Windows Firewall tools](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/tools)
- [Microsoft: Windows Firewall rules](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/rules)
- [Microsoft: Configure Windows Firewall logging](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-logging)
- [Nmap Reference Guide: Firewall and IDS evasion](https://nmap.org/book/man-bypass-firewalls-ids.html)
- [Ncat Users' Guide: Proxying](https://nmap.org/ncat/guide/ncat-proxy.html)
