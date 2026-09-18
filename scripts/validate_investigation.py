#!/usr/bin/env python3
"""Validate the documented SOC investigation against synthetic Zeek-like events."""

import csv
import sys
from collections import defaultdict

events = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8")))
destinations = defaultdict(set)
states = defaultdict(set)
intel = []
for event in events:
    if event["dest_ip"] != "224.0.0.251" and event["approved_scanner"] == "false":
        destinations[event["src_ip"]].add(event["dest_ip"])
        states[event["src_ip"]].add(event["conn_state"])
    if event["intel_match"] == "true":
        intel.append(event)

scan_leads = sorted(src for src, dests in destinations.items() if len(dests) >= 5 and "S0" in states[src])
print("scan_leads=" + ",".join(scan_leads))
print("intel_leads=" + ",".join(sorted({event['src_ip'] for event in intel})))
if scan_leads != ["10.0.0.79"]:
    raise SystemExit("expected one synthetic scan lead")
if {event["src_ip"] for event in intel} != {"10.0.0.142"}:
    raise SystemExit("expected one synthetic intelligence lead")
