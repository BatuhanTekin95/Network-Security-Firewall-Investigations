# Windows Firewall Lab Evidence

This gallery contains the evidence I collected while validating an inbound Windows Firewall rule from a Kali Linux virtual machine. The VM used a bridged adapter so the Windows target and Kali client had different addresses on the same network.

## Lab context

| Item | Value |
| --- | --- |
| Date | 2026-07-15 |
| Windows target | `192.168.1.5` |
| Kali client | `192.168.1.12` |
| Windows profile | Public |
| Test service | TCP 8088 |
| Expected allow result | Port open |
| Expected block result | Connection timeout |

The first Kali allow-test screenshot uses the VM's original `UTC-04:00` timezone. Its timestamp is equivalent to `03:22:56 UTC` and `05:22:56 UTC+02:00`. Later evidence uses the Europe/Berlin timezone directly.

## Evidence sequence

### 1. Baseline firewall profile

The active Public profile was enabled. Allowed and blocked connection logging were disabled before the lab.

![Public firewall profile before the lab](assets/01-baseline-firewall-profile.png)

### 2. Port availability

TCP 8088 was confirmed as available before starting the listener.

![TCP 8088 availability check](assets/02-port-availability.png)

### 3. Logging enabled

Allowed and blocked connection logging were enabled for the Public profile with a 20 MB maximum file size.

![Windows Firewall logging enabled](assets/03-logging-enabled.png)

### 4. Listener active

The Windows host listened on TCP 8088 while the firewall decisions were tested.

![TCP 8088 listener in Listen state](assets/04-listener-active.png)

### 5. Separate Kali client

The bridged Kali VM used a different address and routed directly to the Windows target.

![Kali client address and route to the Windows target](assets/05-kali-client-route.png)

### 6. Allow rule

The inbound allow rule was limited to the Kali source address, TCP 8088 and the Public profile.

![Scoped inbound allow rule](assets/06-allow-rule.png)

### 7. Allowed connection

Netcat reported TCP 8088 as open from the Kali client.

![Successful Kali connection to TCP 8088](assets/07-allow-test.png)

### 8. Block rule

The allow rule was replaced with a block rule using the same source, port and profile scope.

![Scoped inbound block rule](assets/08-block-rule.png)

### 9. Blocked connection

The Kali connection timed out even though the Windows listener remained active.

![Kali connection timeout with the block rule](assets/09-block-test.png)

### 10. Firewall log correlation

The Windows Firewall log recorded DROP and ALLOW events for the same source, destination and destination port.

![Windows Firewall DROP and ALLOW log entries](assets/10-firewall-log.png)

### 11. Cleanup verification

The lab rule was removed, the listener was stopped and Public-profile logging was restored to its baseline values.

![Successful lab cleanup and rollback](assets/11-cleanup.png)

## Conclusion

This test confirmed that a narrowly scoped Windows Firewall rule changed the connection outcome for the same client and service. The Kali results and Windows Firewall records provide two observation points, while the final cleanup output confirms that the temporary configuration did not remain on the host.
