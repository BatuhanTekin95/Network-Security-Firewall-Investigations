# Windows Firewall Rule Validation Lab

**Status:** Completed — 2026-07-15

## Objective

Validate a narrowly scoped inbound rule, collect the related Windows Firewall evidence and return the host to its original state.

## Lab setup

- One Windows 10/11 or Windows Server target
- One Windows or Linux client on the same isolated lab network
- Local administrator access on the Windows target
- An elevated PowerShell session
- TCP port `8088` unused before the test

Do not run this procedure on a production endpoint. Record the target and client IP addresses before starting.

## 1. Capture the baseline

Run on the Windows target:

```powershell
$labGroup = "Portfolio-Firewall-Lab"
$baseline = Get-NetFirewallProfile |
    Select-Object Name, LogAllowed, LogBlocked, LogFileName, LogMaxSizeKilobytes

Get-NetConnectionProfile
Get-NetFirewallProfile |
    Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction,
        LogAllowed, LogBlocked, LogFileName

Get-NetTCPConnection -LocalPort 8088 -ErrorAction SilentlyContinue
```

Expected result: no existing listener on TCP `8088`. If the port is in use, choose another high port and update every command consistently.

## 2. Enable temporary logging

```powershell
Set-NetFirewallProfile -Profile Public `
    -LogAllowed True -LogBlocked True -LogMaxSizeKilobytes 20480
```

The default log path is normally:

```text
%windir%\System32\LogFiles\Firewall\pfirewall.log
```

## 3. Start a temporary listener

Keep this PowerShell window open on the target:

```powershell
$listener = [System.Net.Sockets.TcpListener]::new(
    [System.Net.IPAddress]::Any,
    8088
)
$listener.Start()
$listener.LocalEndpoint
```

## 4. Create and validate an allow rule

In a second elevated PowerShell window on the target:

```powershell
$clientIP = "CLIENT_IP"

New-NetFirewallRule `
    -DisplayName "Lab - Allow TCP 8088" `
    -Group $labGroup `
    -Direction Inbound `
    -Action Allow `
    -Protocol TCP `
    -LocalPort 8088 `
    -RemoteAddress $clientIP `
    -Profile Public
```

From the client:

```powershell
Test-NetConnection -ComputerName TARGET_IP -Port 8088 -InformationLevel Detailed
```

From a Kali or other Linux client:

```bash
date --iso-8601=seconds
nc -nvz -w 3 TARGET_IP 8088
```

Expected result: `TcpTestSucceeded : True` on Windows or `open` with Netcat on Linux.

Record:

- Test time and timezone
- Client and target IP addresses
- `TcpTestSucceeded` result
- Rule name and active Windows network profile
- Matching firewall log line, if recorded

## 5. Replace it with a block rule

Run on the target:

```powershell
Get-NetFirewallRule -Group $labGroup | Remove-NetFirewallRule

New-NetFirewallRule `
    -DisplayName "Lab - Block TCP 8088" `
    -Group $labGroup `
    -Direction Inbound `
    -Action Block `
    -Protocol TCP `
    -LocalPort 8088 `
    -RemoteAddress $clientIP `
    -Profile Public
```

Repeat the client test. The expected result is `TcpTestSucceeded : False` on Windows or a connection timeout on Linux.

## 6. Review evidence

On the target:

```powershell
Get-NetFirewallRule -Group $labGroup |
    Select-Object DisplayName, Enabled, Direction, Action, Profile

Get-Content "$env:windir\System32\LogFiles\Firewall\pfirewall.log" -Tail 100
```

Look for the test timestamp, protocol, source IP, destination IP, destination port and action. If no matching event appears, confirm the active profile, log path, service state and whether another control handled the traffic.

## 7. Cleanup and rollback

Stop the listener in its PowerShell window:

```powershell
$listener.Stop()
```

Remove all rules created by this lab and restore the saved logging settings:

```powershell
Get-NetFirewallRule -Group $labGroup -ErrorAction SilentlyContinue |
    Remove-NetFirewallRule

foreach ($profile in $baseline) {
    Set-NetFirewallProfile `
        -Profile $profile.Name `
        -LogAllowed $profile.LogAllowed `
        -LogBlocked $profile.LogBlocked `
        -LogFileName $profile.LogFileName `
        -LogMaxSizeKilobytes $profile.LogMaxSizeKilobytes
}

Get-NetFirewallRule -Group $labGroup -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 8088 -ErrorAction SilentlyContinue
```

Expected result: neither a lab rule nor a listener remains.

## Recorded results

| Item | Observation |
| --- | --- |
| Lab date and timezone | 2026-07-15, Europe/Berlin (`UTC+02:00`) |
| Target / client | Windows host `192.168.1.5` / Kali Linux VM `192.168.1.12` |
| Virtual network | VirtualBox bridged adapter on the same `/24` network |
| Active firewall profile | Public |
| Test service | TCP listener on `0.0.0.0:8088` |
| Allow test result | Netcat reported TCP 8088 as `open` |
| Block test result | Netcat connection timed out while the listener remained active |
| Matching log evidence | Windows Firewall recorded `DROP` and `ALLOW` for the same source, destination and destination port |
| Cleanup verified | Lab rule removed, listener stopped and logging restored to `False / False / 4096 KB` |

The complete, ordered screenshot set is available in the [Windows Firewall lab evidence gallery](../evidence/windows-firewall-lab/README.md).

The private addresses are retained in the screenshots so the rule, client test and firewall log can be correlated. They are RFC 1918 lab addresses and are not publicly routable.

## References

- [Microsoft: New-NetFirewallRule](https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule)
- [Microsoft: Set-NetFirewallProfile](https://learn.microsoft.com/en-us/powershell/module/netsecurity/set-netfirewallprofile)
- [Microsoft: Configure Windows Firewall logging](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-logging)
