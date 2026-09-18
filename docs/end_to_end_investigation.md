# End-to-End SOC Investigation: Discovery and Intelligence Leads

## Executive disposition

Synthetic Zeek-like telemetry produced two separate investigation leads: repeated failed SMB connections from `10.0.0.79`, consistent with a Network Service Discovery hypothesis, and a moderate-confidence intelligence match involving `10.0.0.142`. Neither lead alone proves compromise. The evidence supports targeted endpoint and identity correlation before incident declaration.

## Detection logic

The SPL excludes multicast and approved scanners, groups activity by source, and identifies a discovery lead when a source reaches at least five unique destinations with `S0` connection states. A separate enrichment condition retains recent moderate- or high-confidence intelligence matches. The threshold is intentionally low for a seven-event demonstration dataset and must be baselined before production use.

## Workflow and evidence

| Step | Evidence | Decision |
|---|---|---|
| Normalize | Seven synthetic Zeek-like connection events | Fields are sufficient for a controlled test |
| Detect | Five failed SMB connections from `10.0.0.79` to distinct destinations | Open discovery hypothesis |
| Enrich | `10.0.0.142` connected to a synthetic moderate-confidence intelligence match | Prioritize contextual review |
| Reduce noise | Multicast `224.0.0.251:5353` excluded | Treat expected mDNS as benign for this test |
| Map behavior | Repeated destination discovery pattern | Candidate MITRE ATT&CK T1046 |
| Disposition | No endpoint, user, or command-line evidence | Investigative leads; no confirmed incident |

## Reproduction

```bash
python scripts/validate_investigation.py data/synthetic_zeek_investigation.csv
```

Expected output:

```text
scan_leads=10.0.0.79
intel_leads=10.0.0.142
```

Load the CSV as the Splunk lookup `synthetic_zeek_investigation.csv`, then run `splunk_queries/validated_investigation.spl`.

## Escalation and next collection

For `10.0.0.79`, collect endpoint process creation, authenticated user, approved administration activity, and five-minute destination baselines. For `10.0.0.142`, preserve intelligence source, indicator age, confidence, asset criticality, and endpoint/network corroboration. Escalate only if those sources support unauthorized discovery or malicious infrastructure use.

## False-positive considerations

- authorized vulnerability scanners and inventory tools;
- patching or systems-management traffic;
- short-lived lab simulations;
- recycled or shared intelligence infrastructure; and
- incomplete connections caused by filtering or packet loss.

## Portfolio value

This case demonstrates the analyst loop: hypothesis, reproducible SPL, noise reduction, intelligence enrichment, ATT&CK mapping, confidence boundary, disposition, and evidence-driven next action.
