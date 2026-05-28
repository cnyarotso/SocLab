# SOC Workflow Notes

## What This Lab Simulates

This lab simulates the beginning of a real SOC workflow:

```text
Traffic → Packet Capture → Zeek Logs → Splunk SIEM → Search/Dashboard/Alerting
```

## Analyst Workflow

A SOC analyst typically does not watch raw packets all day. Instead:

1. Tools collect telemetry.
2. SIEM platforms ingest logs.
3. Alerts or dashboards highlight suspicious behavior.
4. Analysts investigate using searches and pivots.
5. Packet tools like Wireshark are used for deep inspection.

## What Splunk Adds

Splunk centralizes logs and allows analysts to:

- Search events
- Extract fields
- Build dashboards
- Create alerts
- Correlate activity across sources
