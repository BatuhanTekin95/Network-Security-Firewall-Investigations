# Firewall Detection Notes

These are starter queries for lab data and detection development. They are not presented as production-ready rules. Field names, normal values and thresholds must be mapped to the environment before use.

## Minimum normalized fields

| Concept | Example normalized field |
| --- | --- |
| Event time | `_time` / `@timestamp` |
| Device | `device_name` |
| Action | `action` |
| Source | `src_ip`, `src_port`, `src_zone` |
| Destination | `dest_ip`, `dest_port`, `dest_zone` |
| Network | `transport`, `bytes`, `packets`, `duration` |
| Policy | `rule_name`, `rule_id`, `policy_version` |
| Translation | `nat_src_ip`, `nat_dest_ip` |
| Application | `application`, `user` |

Before using a query, I verify whether `deny`, `denied`, `drop` and `blocked` have been normalized into one action value.

## Detection 1: one source probing many ports

**Question:** Is one source producing denied connections to many destination ports in a short period?

```spl
index=firewall action IN ("deny", "denied", "drop", "blocked")
| bin _time span=5m
| stats count dc(dest_port) AS distinct_ports values(dest_port) AS ports
    BY _time src_ip dest_ip
| where distinct_ports >= 15 AND count >= 20
| sort - distinct_ports
```

Possible false positives include vulnerability scanners, monitoring systems and approved administration tools. I would tune this query with asset role and scanner allowlists rather than suppressing all internal sources.

## Detection 2: many sources targeting one service

**Question:** Is a destination receiving denied connections from many sources on the same port?

```spl
index=firewall action IN ("deny", "denied", "drop", "blocked")
| bin _time span=10m
| stats count dc(src_ip) AS distinct_sources values(src_ip) AS sources
    BY _time dest_ip dest_port
| where distinct_sources >= 20 AND count >= 30
| sort - distinct_sources
```

This may identify internet background scanning as well as focused activity. Asset exposure, geolocation and the expected service should influence severity.

## Detection 3: denied traffic followed by an allowed connection

**Question:** Did a source receive several denies and then reach the same destination and port?

```spl
index=firewall action IN ("allow", "allowed", "accept", "deny", "denied", "drop", "blocked")
| eval outcome=if(action IN ("allow", "allowed", "accept"), "allowed", "denied")
| bin _time span=10m
| stats count(eval(outcome="denied")) AS denies
    count(eval(outcome="allowed")) AS allows
    min(_time) AS first_seen max(_time) AS last_seen
    BY src_ip dest_ip dest_port
| where denies >= 5 AND allows >= 1
| convert ctime(first_seen) ctime(last_seen)
| sort - denies
```

This query is a triage lead, not proof of a bypass. Rule changes, load balancers, failover paths or mixed devices can produce the same pattern.

## Elastic KQL starting points

Repeated denied network activity:

```kql
event.dataset : *firewall* and event.action : (deny or denied or drop or blocked)
```

Allowed outbound traffic on a locally defined watchlist of unusual ports:

```kql
event.dataset : *firewall* and event.action : (allow or allowed or accept)
and network.direction : outbound
and destination.port : (4444 or 5555 or 6667 or 9001)
```

KQL filters select candidate events; aggregation, thresholds and alert suppression should be configured in the detection rule. A port list must be based on the environment, not copied as a universal definition of malicious traffic.

## Triage checklist

1. Confirm timezone, sensor health and data completeness.
2. Identify the device, rule and policy version that produced the event.
3. Check whether addresses are pre-NAT or post-NAT.
4. Compare the destination port with the detected application.
5. Review the same source across DNS, proxy, VPN and endpoint logs.
6. Determine whether the asset is expected to expose or use the service.
7. Document the reason for escalation or closure.

## Tuning record

For each detection I plan to record:

- Data source and field mapping
- Baseline period
- Threshold rationale
- Known scanners and business exceptions
- Example true-positive and false-positive events
- Last review date

This keeps query changes explainable and prevents an arbitrary threshold from looking more certain than it is.
