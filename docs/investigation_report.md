# Investigation Report

## Question

Which source hosts and connection states in the Zeek `conn.log` data warrant follow-up, and does the available evidence justify escalation?

## Scope

- Source: lab-generated packet capture
- Primary telemetry: Zeek `conn.log`
- Supporting telemetry: summarized `dns.log` observations
- Analysis platform: Splunk
- Environment: small home/lab network
- Excluded context: endpoint, identity, vulnerability, asset criticality, and external intelligence feeds

## Hypotheses

1. A source contacting many destinations in a short period may indicate scanning or automated discovery.
2. Repeated `S0`, `OTH`, or `SHR` states may indicate failed probing, filtering, packet loss, or normal application behavior.
3. Multicast DNS traffic is likely expected local discovery unless its volume, source, or timing is abnormal.

## Evidence reviewed

| Evidence | Use |
|---|---|
| `conn.log` | Source/destination, ports, protocol, volume, and connection state |
| `dns.log` observations | Distinguish local discovery from external DNS behavior |
| Splunk screenshots | Confirm ingestion, field extraction, aggregation, and visualization |
| SPL query files | Make analysis reproducible and reviewable |

## Analysis

The connection data included common HTTPS and DNS traffic as well as `S0`, `OTH`, and `SHR` states. Those states can be useful for hunting, but none is malicious by definition. They must be assessed by frequency, destination diversity, destination port, asset role, and time window.

The DNS observations included UDP/5353 traffic, multicast destinations `224.0.0.251` and `ff02::fb`, and `.local` names. This pattern is consistent with mDNS-based device discovery on a local network.

A source-host ranking identifies where an analyst should begin, but raw event count is not a severity score. The updated queries add unique-destination and time-window context so the ranking can support a testable hypothesis.

## Disposition

| Item | Disposition | Confidence |
|---|---|---|
| Local mDNS discovery | Expected/benign in this lab context | Moderate |
| Incomplete connection states | Investigative lead; insufficient for escalation | Moderate |
| Network scanning | Not established by current evidence | Moderate |
| Confirmed compromise | Not supported | High |

## Next actions

1. Add destination and destination-port distributions to every source-host review.
2. Baseline unique destinations per five-minute window.
3. Exclude approved scanners, infrastructure services, and multicast traffic.
4. Correlate external destinations and DNS queries with intelligence that includes provenance, confidence, and indicator age.
5. Add endpoint and identity telemetry for the highest-priority host.
6. Convert a hypothesis into an alert only after testing false positives against representative data.

## Communication note

The decision is deliberately conservative: the pipeline surfaced hunting leads, but the available context is insufficient for attribution or incident declaration. This protects credibility while specifying exactly what evidence would change the decision.
