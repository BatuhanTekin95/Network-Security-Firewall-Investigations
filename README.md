# Firewall Technologies and Security Monitoring

This repository is where I document my firewall studies from a SOC analyst's point of view. The focus is not only on how firewall rules work, but also on what their logs can tell an analyst during triage and investigation.

## Current content

| Module | Focus | Status |
| --- | --- | --- |
| [Firewall Fundamentals and Administration](docs/Firewall-Fundamentals-and-Administration.md) | Firewall types, rule evaluation, Windows Firewall, NGFW capabilities, evasion limits and log analysis | Complete |
| [Windows Firewall Rule Validation Lab](labs/Windows-Firewall-Rule-Validation.md) | Controlled allow/block test, firewall log correlation and verified rollback | Completed |
| [Firewall Detection Notes](detections/README.md) | Normalized fields, triage workflow and starter SIEM queries | Draft detections |

The status labels are intentional. A lab marked **Completed** includes dated evidence and verified cleanup. Draft detections still require environment-specific field mapping and tuning.

## What I am practising

- Reading firewall policy as ordered, state-aware traffic decisions
- Separating filtering rules from routing, NAT and port-forwarding functions
- Validating Windows Firewall changes safely and documenting rollback
- Reviewing allowed and denied connections in context
- Turning firewall telemetry into investigation questions and detection ideas
- Recording limitations instead of treating a single log source as proof

## Repository structure

```text
.
|-- docs/          # Technical notes and concepts
|-- labs/          # Reproducible exercises with cleanup steps
|-- detections/    # SOC triage notes and starter SIEM queries
|-- .github/       # Documentation quality checks
|-- LICENSE
`-- README.md
```

## Investigation approach

My basic workflow is:

1. Confirm the time range, affected host and network direction.
2. Review the firewall action and the rule that produced it.
3. Group repeated activity by source, destination, port and time window.
4. Compare the traffic with endpoint, DNS, proxy and authentication evidence.
5. Record what is known, what is inferred and what still needs validation.

## Scope and safety

The commands and evasion examples in this repository are for systems I own or have explicit permission to test. The practical lab uses a controlled network and includes cleanup steps. The detection queries are starting points and require field mapping and tuning before production use.

## Related projects

- [Detection Engineering](https://github.com/BatuhanTekin95/Detection-Engineering)
- [SIEM Investigation Case Studies](https://github.com/BatuhanTekin95/SIEM-Investigation-Case-Studies)
- [SOC Phishing Case Studies](https://github.com/BatuhanTekin95/SOC-Phishing-Case-Studies)

## License

This project is available under the [MIT License](LICENSE).
